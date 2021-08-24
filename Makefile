#------------------------------------------------------------------------------
# Build-specific Variables
#------------------------------------------------------------------------------

ifndef DFTPL_GEN_DIR
  $(error `DFTPL_GEN_DIR` must be set to a writable directory for generated source files!)
endif

ifndef DFTPL_GEN_LIST
  $(info `DFTPL_GEN_LIST` may be set to a writable filename to create a list of generated files.)
endif

ifndef DFTPL_CONFIG
  $(error `DFTPL_CONFIG` must be set to the name of the toplevel config file in the default module!)
endif

ifndef DFTPL_CFGDIRS
  $(error `DFTPL_CFGDIRS` must be set to a list of directories with config files for the default module.)
endif

ifndef DFTPL_TPLDIRS
  $(warning `DFTPL_TPLDIRS` should be set to a list of directories with template files for the default module.)
endif

ifndef DFTPL_MODULES
  $(info `DFTPL_MODULES` may be set to a list of module names to include non-default modules.)
endif

#TODO-lw also check $(DFTPL_CFGDIRS_$(mod)) and $(DFTPL_TPLDIRS_$(mod)) adaptively

GENARGS  = -o $(DFTPL_GEN_DIR)
ifdef DFTPL_GEN_LIST
GENARGS += -l $(DFTPL_GEN_LIST)
endif
GENARGS += -e $(DFTPL_CONFIG)
GENARGS += $(foreach dir,$(DFTPL_TPLDIRS),-t $(dir))
GENARGS += $(foreach dir,$(DFTPL_CFGDIRS),-c $(dir))
GENARGS += $(foreach mod,$(DFTPL_MODULES),-m $(mod) \
              $(foreach dir,$(DFTPL_TPLDIRS_$(mod)),-t $(dir)) \
              $(foreach dir,$(DFTPL_CFGDIRS_$(mod)),-c $(dir)))


#------------------------------------------------------------------------------
# Project-specific Variables
#------------------------------------------------------------------------------

PYTHON  ?= python3
VENV_DIR = $(abspath ./.venv)
VPYTHON  = $(VENV_DIR)/bin/python


#------------------------------------------------------------------------------
# User Information
#------------------------------------------------------------------------------

.PHONY: usage
usage:
	@echo "Usage:"
	@echo " make usage   - Display this info panel"
	@echo " make info    - Display build variables"
	@echo " make tpl     - Render templates to generate source files"
	@echo " make update  - Delete Python environment to reinstall DFACCTO-TPL module"
	@echo " make clean   - Delete generated hardware sources"
	@echo
	@echo "Environment:"
	@echo " DFTPL_GEN_DIR       - Writable directory for generated source files"
	@echo " DFTPL_GEN_LIST      - Filename for a list of generated source files"
	@echo " DFTPL_CONFIG        - Name of the toplevel config file, searched in the default module"
	@echo " DFTPL_CFGDIRS       - List of directories with config files for the default module"
	@echo " DFTPL_TPLDIRS       - List of directories with template files for the default module"
	@echo " DFTPL_MODULES       - List of names for additional modules"
	@echo " DFTPL_CFGDIRS_<mod> - List of directories with config files for module <mod>"
	@echo " DFTPL_TPLDIRS_<mod> - List of directories with template files for module <mod>"

.PHONY: info
info:
	@echo "Variables:"
	@echo " DFTPL_GEN_DIR  = $(DFTPL_GEN_DIR)"
	@echo " DFTPL_GEN_LIST = $(DFTPL_GEN_LIST)"
	@echo
	@echo " DFTPL_CONFIG   = $(DFTPL_CONFIG)"
	@echo " DFTPL_MODULES  = $(DFTPL_MODULES)"
	@echo " DFTPL_CFGDIRS  = $(DFTPL_CFGDIRS)"
	@echo -e " $(foreach mod,$(DFTPL_MODULES),DFTPL_CFGDIRS_$(mod) = $(DFTPL_CFGDIRS_$(mod))\\n)"
	@echo " DFTPL_TPLDIRS  = $(DFTPL_TPLDIRS)"
	@echo -e " $(foreach mod,$(DFTPL_MODULES),DFTPL_TPLDIRS_$(mod) = $(DFTPL_TPLDIRS_$(mod))\\n)"
	@echo
	@echo " GENARGS        = $(GENARGS)"
	@echo " PYTHON         = $(PYTHON)"
	@echo " VENV_DIR       = $(VENV_DIR)"
	@echo " VPYTHON        = $(VPYTHON)"

#------------------------------------------------------------------------------
# Hardware Sources
#------------------------------------------------------------------------------

$(VENV_DIR): .
	@echo
	@echo "--- Initialize template toolchain"
	@$(PYTHON) -m venv $(VENV_DIR)
	@touch $(VENV_DIR)
	@$(VPYTHON) -m pip install --upgrade pip
	@$(VPYTHON) -m pip install .
	@echo

.PHONY: tpl
tpl: $(DFTPL_GEN_LIST)

.PHONY: $(DFTPL_GEN_LIST)
$(DFTPL_GEN_LIST): $(VENV_DIR)
	@echo
	@echo "--- Generating hardware sources"
	@mkdir -p $(DFTPL_GEN_DIR)
	@$(VPYTHON) -m dfaccto_tpl $(GENARGS)
	@echo


.PHONY: update
update:
	@git pull || true
ifdef VENV_DIR
	@rm -rf $(VENV_DIR)
endif

#------------------------------------------------------------------------------
# Cleanup
#------------------------------------------------------------------------------

.PHONY: clean
clean:
ifdef DFTPL_GEN_LIST
	rm -f  $(DFTPL_GEN_LIST)
endif
ifdef DFTPL_GEN_DIR
	rm -rf $(DFTPL_GEN_DIR)/*
endif


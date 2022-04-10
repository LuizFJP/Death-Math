import cx_Freeze

executables = [cx_Freeze.Executable('DeathMath.py')]

cx_Freeze.setup(
  name="Death Math",
  options = {'build_exe': {'include_msvcr': {'packages': ['pygame'],
  'include_files': ['media']
  }}},
  executables = executables
)
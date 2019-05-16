from buildbot.util import NotABranch
from buildbot.changes import filter


class ChangeFilter(filter.ChangeFilter):
    """Extended with ability to filter on properties"""

    def __init__(self, fn=None, branch=NotABranch, project=None,
                 repository=None, category=None, codebase=None,
                 properties=None):
        if fn is not None and not callable(fn):
            raise ValueError('ChangeFilter.fn must be callable')

        properties = properties or {}
        if not isinstance(properties, dict):
            raise ValueError('ChangeFilter.properties must be a dictionary')

        # create check tuples for the original arguments
        # branch has a special treatment beacuase of NotABranch
        checks = [
            self._create_check_tuple('branch', branch, default=NotABranch),
            self._create_check_tuple('project', project),
            self._create_check_tuple('repository', repository),
            self._create_check_tuple('category', category),
            self._create_check_tuple('codebase', codebase)
        ]

        # create check tuples for the properties argument
        checks += [self._create_check_tuple(f'prop:{name}', value)
                   for name, value in properties.items()]

        self.filter_fn = fn
        self.checks = self.createChecks(*checks)

    def _create_check_tuple(self, name, value, default=None):
        # sample: (project, project_re, project_fn, "project"),
        if callable(value):
            return (default, None, value, name)
        elif hasattr(value, 'match'):
            return (default, value, None, name)
        else:
            return (value, None, None, name)
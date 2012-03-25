import os
from urwid import AttrSpec, AttrSpecError

from utils import read_config
from errors import ConfigError
from configobj import ConfigObj

DEFAULTSPATH = os.path.join(os.path.dirname(__file__), '..', 'defaults')


class Theme(object):
    """Colour theme"""
    def __init__(self, path):
        """
        :param path: path to theme file
        :type path: str
        :raises: :class:`~alot.settings.errors.ConfigError`
        """
        self._spec = os.path.join(DEFAULTSPATH, 'theme.spec')
        self._config = read_config(path, self._spec)
        self.attributes = self._parse_attributes(self._config)

    def _parse_attributes(self, c):
        """
        parse a (previously validated) valid theme file
        into urwid AttrSpec attributes for internal use.

        :param c: config object for theme file
        :type c: `configobj.ConfigObj`
        :raises: `ConfigError`
        """

        attributes = {}
        for sec in c.sections:
            try:
                colours = int(sec)
            except ValueError:
                err_msg = 'section name %s is not a valid colour mode'
                raise ConfigError(err_msg % sec)
            attributes[colours] = {}
            for mode in c[sec].sections:
                attributes[colours][mode] = {}
                if mode == 'search':
                    for tline in c[sec][mode].sections:
                        attributes[colours][mode][tline] = {}
                        order = c[sec][mode][tline]['order']
                        attributes[colours][mode][tline]['order'] = order

                        sf = self._read_attribute(c, [mode, tline], colours,
                                                  suffix='_focus')
                        sn = self._read_attribute(c, [mode, tline], colours)
                        spaces = {'normal': sn, 'focus': sf}
                        attributes[colours][mode][tline]['spaces'] = spaces

                        config_sec = c[sec][mode][tline]
                        internal_sec = attributes[colours][mode][tline]
                        for themable in config_sec.sections:
                            internal_sec[themable] = {}
                            att = self._read_attribute(c,
                                                       [mode, tline, themable],
                                                       colours)
                            internal_sec[themable]['normal'] = att
                            att = self._read_attribute(c,
                                                       [mode, tline, themable],
                                                       colours, '_focus')
                            internal_sec[themable]['focus'] = att
                            fixed = config_sec[themable]['width_fixed']
                            weight = config_sec[themable]['width_weight']
                            if fixed != None:
                                widthtuple = (fixed,)
                            elif weight != None:
                                widthtuple = ()
                            else:
                                widthtuple = ('pack',)
                            internal_sec[themable]['widthtuple'] = widthtuple

                else:
                    for themable in c[sec][mode].sections:
                        att = self._read_attribute(c, [mode, themable],
                                                   colours)
                        attributes[colours][mode][themable] = att
        return attributes

    def _read_attribute(self, cfg, path, colours, suffix=''):
        bg = 'default'
        if colours != 1:
            lpath = [str(colours)] + path + ['bg' + suffix]
            bg = self._get_leaf_value(cfg, lpath)
            if bg == None:
                if colours == 16:
                    lpath = ['1'] + path + ['bg' + suffix]
                    bg = self._get_leaf_value(cfg, lpath)
                else:
                    lpath =  ['16'] + path + ['bg' + suffix]
                    bg = self._get_leaf_value(cfg, lpath)
        bg = bg or 'default'

        lpath = [str(colours)] + path + ['fg' + suffix]
        fg = self._get_leaf_value(cfg, lpath)
        if fg == None:
            if colours == 16:
                lpath = ['1'] + path + ['fg' + suffix]
                fg = self._get_leaf_value(cfg, lpath)
            else:
                lpath =  ['16'] + path + ['fg' + suffix]
                fg = self._get_leaf_value(cfg, lpath)
        fg = fg or 'default'

        try:
            att = AttrSpec(fg, bg, colours)
        except AttrSpecError, e:
            raise ConfigError(e)
        return att

    def _get_leaf_value(self, cfg, path):
        if len(path) == 1:
            if isinstance(cfg, ConfigObj):
                if path[0] not in cfg.scalars:
                    return None
                else:
                    return cfg[path[0]]
            else:
                if path[0] not in cfg:
                    return None
                else:
                    return cfg[path[0]]
        else:
            scfg = cfg[path[0]]
            sp = path[1:]
            return self._get_leaf_value(scfg, sp)

    def get_threadline_structure(self, thread, colourmode):
        return self.attributes[colourmode]['search']['threadline']

    def get_attribute(self, path):
        """
        returns requested attribute
        """
        return self._get_leaf_value(self.attributes, path)


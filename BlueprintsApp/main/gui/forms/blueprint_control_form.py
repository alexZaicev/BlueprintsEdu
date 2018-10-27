from gui.forms.form import Form
from utils.gui_utils import Themes
from utils import logger_utils
import pygame as pg
from pygame.locals import *
from utils.string_utils import StringUtils
from gui.blueprints.attribute_blueprint import AttributeBlueprint


class BlueprintControlForm(Form):

    def __init__(self, control_panel, display, coords=None, size=None):
        Form.__init__(self, display, coords, size)
        self.__cont_panel = control_panel
        self.__logger = logger_utils.get_logger(__name__)
        self.__bps = list()
        self.__bps_connections = list()

    def draw_form(self):
        pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("panel_disabled"), self.get_rect(), 0)
        if self.get_rect().collidepoint(pg.mouse.get_pos()) == 1:
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("selection_background"), self.get_rect(), 2)
        self.draw_connections()
        if len(self.__bps) > 0:
            for bp in self.__bps:
                if not bp.focused:
                    pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("idle_blueprint"), bp.get_rect(), 0)
                else:
                    pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("enabled_blueprint"), bp.get_rect(), 0)
                self.display.blit(bp.get_text(), bp.get_text_rect())
                if bp.is_hovered():
                    pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("selection_background"), bp.get_rect(), 2)

    def draw_connections(self):
        for con in self.__bps_connections:
            c1 = con[0].get_rect().center
            c2 = con[1].get_rect().center
            pg.draw.line(self.display, Themes.DEFAULT_THEME.get("connection_line"), c1, c2, 2)

    def unfocuse_blueprints(self):
        self.__cont_panel.set_blueprint(None)
        if len(self.__bps) > 0:
            for bp in self.__bps:
                bp.focused = False

    def check_form_events(self, event):
        super().check_form_events(event)
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:   # LEFT MOUSE BUTTON
                self.unfocuse_blueprints()
                pos = pg.mouse.get_pos()
                if len(self.__bps) > 0:
                    for bp in self.__bps:
                        if bp.get_rect().collidepoint(pos) == 1:
                            bp.pressed = True
                            self.__logger.debug("Pressed true")
                            bp.set_offset(pos)
                            if not bp.focused:
                                bp.focused = True
                                self.__cont_panel.set_blueprint(bp)
                            break
            elif event.button == 3:  # RIGHT MOUSE BUTTON
                pos = pg.mouse.get_pos()
                if len(self.__bps) > 0:
                    for bp in self.__bps:
                        if bp.get_rect().collidepoint(pos) == 1:
                            if not bp.connected:
                                for bp_1 in self.__bps:
                                    if bp != bp_1 and bp_1.focused and not bp_1.connected:
                                        # TODO check for valid blueprint type connection
                                        bp.connected = True
                                        bp_1.connected = True
                                        self.__bps_connections.append([bp, bp_1])

        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:   # LEFT MOUSE BUTTON
                self.__logger.debug("MOUSEBUTTONUP")
                pos = pg.mouse.get_pos()
                if len(self.__bps) > 0:
                    for bp in self.__bps:
                        if bp.get_rect().collidepoint(pos) == 1:
                            self.__logger.debug("Pressed false")
                            bp.pressed = False
                            break
        elif event.type == MOUSEMOTION:
            if len(self.__bps) > 0:
                for bp in self.__bps:
                    if bp.pressed:
                        mx, my = event.pos
                        bp.set_topleft((mx + bp.offset[0], my + bp.offset[1]))
                        self.__check_blueprint_inbound(bp)
                        self.__logger.debug(bp.get_rect().topleft)

    def __check_blueprint_inbound(self, blueprint):
        r = self.get_rect()
        bp = blueprint.get_rect()
        left, top = bp.left, bp.top
        if r.left > bp.left:
            left = r.left
        if r.right < bp.right:
            left = r.right - bp.width
        if r.top > bp.top:
            top = r.top
        if r.bottom < bp.bottom:
            top = r.bottom - bp.height
        blueprint.set_topleft((left, top))

    def add_attribute(self):
        t = AttributeBlueprint(self.get_rect(), None)
        self.__bps.append(t)

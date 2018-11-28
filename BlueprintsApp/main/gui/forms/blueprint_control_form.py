import pygame as pg
from pygame.locals import *

from blueprints.attribute_blueprint import AttributeBlueprint as AB
from blueprints.blueprint import Blueprint
from blueprints.character_blueprint import CharacterBlueprint as CB
from blueprints.function_blueprint import FunctionBlueprint as FB
from blueprints.sprite_blueprint import SpriteBlueprint as SB
from gui.blueprints.attribute_blueprint import AttributeBlueprint
from gui.blueprints.character_blueprint import CharacterBlueprint
from gui.blueprints.function_blueprint import FunctionBlueprint
from gui.blueprints.sprite_blueprint import SpriteBlueprint
from gui.blueprints.system_blueprint import SystemBlueprint
from gui.forms.form import Form
from gui.popup import Popup
from utils import logger_utils
from utils.app_utils import BlueprintError
from utils.gui_utils import Themes
from utils.managers.blueprint_manager import BlueprintManager
from utils.managers.execution_manager import ExecutionManager
from utils.managers.project_manager import ProjectManager


class BlueprintControlForm(Form):

    def __init__(self, control_panel, display, project_info, generated, coords=None, size=None):
        Form.__init__(self, display, coords, size)
        self.__project_info = project_info
        self.__cont_panel = control_panel
        self.__logger = logger_utils.get_logger(__name__)
        self.__bps = list()
        self.__bps_connections = list()
        self.generated = generated
        self.popup = None

    def update_form(self, coords=None, size=None):
        super().update_form(coords, size)

    def check_system_exist(self):
        for bp in self.__bps:
            if isinstance(bp, SystemBlueprint):
                return True
        else:
            return False

    def get_system_blueprint(self):
        for bp in self.__bps:
            if isinstance(bp, SystemBlueprint):
                return bp.get_blueprint()
        else:
            return None

    def draw_form(self):
        pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("panel_disabled"), self.get_rect(), 0)
        if self.get_rect().collidepoint(pg.mouse.get_pos()) == 1:
            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("selection_background"), self.get_rect(), 2)
        self.draw_connections()
        if len(self.__bps) > 0:
            for bp in self.__bps:
                if bp.get_blueprint().get_type() == Blueprint.TYPES.get("CHARACTER"):
                    # CHARACTER ALIVE STATE COLOR IDENTIFICATION
                    if not bp.focused:
                        if bp.get_blueprint().alive:
                            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("active_blueprint"), bp.get_rect(), 0)
                        else:
                            pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("idle_blueprint"), bp.get_rect(), 0)
                    else:
                        pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("enabled_blueprint"), bp.get_rect(), 0)
                else:
                    if not bp.focused:
                        pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("idle_blueprint"), bp.get_rect(), 0)
                    else:
                        pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("enabled_blueprint"), bp.get_rect(), 0)
                self.display.blit(bp.get_text(), bp.get_text_rect())
                if bp.is_hovered():
                    pg.draw.rect(self.display, Themes.DEFAULT_THEME.get("selection_background"), bp.get_rect(), 2)
                self.draw_blueprint_data(bp)
        if self.popup is not None:
            self.popup.draw(self.display)

    def draw_blueprint_data(self, blueprint):
        func_calls = {
            Blueprint.TYPES.get("FUNCTION"): self.draw_function_data,
            Blueprint.TYPES.get("SPRITE"): self.draw_sprite_data,
            Blueprint.TYPES.get("CHARACTER"): self.draw_character_data,
            Blueprint.TYPES.get("ATTRIBUTE"): self.draw_attribute_data,
            Blueprint.TYPES.get("SYSTEM"): self.draw_system_data
        }
        bp_type = blueprint.get_blueprint().get_type()
        try:
            func_calls[bp_type](blueprint)
        except KeyError:
            self.__logger.error("Unknown blueprint type [{}]".format(bp_type))

    def draw_attribute_data(self, blueprint):
        bp_data = blueprint.get_blueprint()
        txt = blueprint.font.render("{} :: {}".format(bp_data.get_data_type(), bp_data.get_value()), True,
                                    Themes.DEFAULT_THEME.get("font"))
        rect_txt = txt.get_rect()
        rect_txt.centerx = blueprint.get_rect().centerx
        rect_txt.centery = int(blueprint.get_rect().centery + blueprint.get_rect().height * .2)
        self.display.blit(txt, rect_txt)

    def draw_character_data(self, blueprint):
        pass

    def draw_sprite_data(self, blueprint):
        pass

    def draw_function_data(self, blueprint):
        pass

    def draw_system_data(self, blueprint):
        pass

    def draw_connections(self):
        self.update_connections()
        for root, slave in self.__bps_connections:
            if root is not None and slave is not None:
                c1 = root.get_rect().center
                c2 = slave.get_rect().center
                pg.draw.line(self.display, Themes.DEFAULT_THEME.get("connection_line"), c1, c2, 2)

    def unfocus_blueprints(self):
        self.__cont_panel.set_blueprint(None)
        if len(self.__bps) > 0:
            for bp in self.__bps:
                bp.focused = False

    def check_form_events(self, event):
        super().check_form_events(event)
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # LEFT MOUSE BUTTON
                pos = pg.mouse.get_pos()
                if len(self.__bps) > 0:
                    for bp in self.__bps:
                        if bp.get_rect().collidepoint(pos) == 1:
                            bp.pressed = True
                            bp.set_offset(pos)
                            if not bp.focused:
                                self.unfocus_blueprints()
                                bp.focused = True
                                self.__cont_panel.set_blueprint(bp)
                            elif bp.focused:
                                self.unfocus_blueprints()
                            break
            elif event.button == 3:  # RIGHT MOUSE BUTTON
                pos = pg.mouse.get_pos()
                if len(self.__bps) > 0:
                    for bp in self.__bps:
                        if bp.get_rect().collidepoint(pos) == 1:
                            for bp_1 in self.__bps:
                                if bp != bp_1 and bp_1.focused:
                                    self.connect_blueprints(bp_1, bp)

        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:  # LEFT MOUSE BUTTON
                pos = pg.mouse.get_pos()
                if len(self.__bps) > 0:
                    for bp in self.__bps:
                        if bp.get_rect().collidepoint(pos) == 1:
                            bp.pressed = False
                            break
        elif event.type == MOUSEMOTION:
            if len(self.__bps) > 0:
                for bp in self.__bps:
                    if bp.pressed:
                        mx, my = event.pos
                        bp.set_topleft((mx + bp.offset[0], my + bp.offset[1]))
                        self.__check_blueprint_inbound(bp)

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
        if self.check_system_exist():
            t = AttributeBlueprint(self.get_rect())
            self.__bps.append(t)
        else:
            raise BlueprintError("Project must include system representation")

    def add_character(self):
        if self.check_system_exist():
            t = CharacterBlueprint(self.get_rect())
            t.parent = self.get_system_blueprint()
            self.__bps.append(t)
        else:
            raise BlueprintError("Project must include system representation")

    def add_function(self, fun_type):
        if self.check_system_exist():
            t = FunctionBlueprint(self.get_rect())
            t.get_blueprint().func_type = fun_type
            self.__bps.append(t)
        else:
            raise BlueprintError("Project must include system representation")

    def add_sprite(self):
        if self.check_system_exist():
            t = SpriteBlueprint(self.get_rect())
            t.parent = self.get_system_blueprint()
            self.__bps.append(t)
        else:
            raise BlueprintError("Project must include system representation")

    def add_system(self):
        if not self.check_system_exist():
            t = SystemBlueprint(self.get_rect())
            self.__bps.append(t)
        else:
            raise BlueprintError("Project must have only one instance of a system")

    def save_project(self):
        """Description: function prepares blueprints in the current development
        panel for further processing
        """
        data = list()
        for bp in self.__bps:
            d = list()

            d.append(bp.get_blueprint())
            r = bp.get_rect()
            d.append([r.topleft, r.size])

            data.append(d)
        ProjectManager.save_project(self.__project_info, data, self.__bps_connections, self.generated)

    def load_project(self, bp_conn, bps):
        self.__bps = BlueprintManager.reverse_parse_blueprints(self.get_rect(), bps)
        self.__logger.debug(self.__bps)
        self.__bps_connections = BlueprintManager.generate_connections(bp_conn, self.__bps)

    def get_project_dict(self):
        r = dict()
        r["PROJECT"] = self.__project_info
        a, c, f, s = list(), list(), list(), list()
        for bp in self.__bps:
            if isinstance(bp.get_blueprint(), AB):
                a.append(bp.get_blueprint())
            elif isinstance(bp.get_blueprint(), FB):
                f.append(bp.get_blueprint())
            elif isinstance(bp.get_blueprint(), SB):
                s.append(bp.get_blueprint())
            elif isinstance(bp.get_blueprint(), CB):
                c.append(bp.get_blueprint())
        r["ATTRIBUTES"] = a
        r["FUNCTIONS"] = f
        r["CHARACTERS"] = c
        r["SPRITES"] = s
        return r

    def execute_project(self):
        try:
            ExecutionManager.execute_program(self.__project_info[0], "app")
            self.__logger.info("Project`s [{}] app.py started".format(self.__project_info[0]))
        except FileNotFoundError as ex:
            self.popup = Popup(Popup.POP_STATES.get("ERROR"), str(ex))

    def clear_connections(self):
        self.__bps_connections.clear()
        for bp in self.__bps:
            if isinstance(bp, CharacterBlueprint) or isinstance(bp, SpriteBlueprint):
                bp.get_blueprint().clear_connections()
        self.__logger.debug("Connections cleared")

    def connect_blueprints(self, bp_1, bp_2):
        valid = True
        type_1 = bp_1.get_blueprint().get_type()
        type_2 = bp_2.get_blueprint().get_type()
        if type_1 == Blueprint.TYPES.get("ATTRIBUTE"):
            if (type_2 == Blueprint.TYPES.get("ATTRIBUTE")) or \
                    (type_2 == Blueprint.TYPES.get("FUNCTION")):
                valid = False
        if type_1 == Blueprint.TYPES.get("CHARACTER"):
            if type_2 == Blueprint.TYPES.get("CHARACTER"):
                valid = False
        if type_1 == Blueprint.TYPES.get("FUNCTION"):
            if (type_2 == Blueprint.TYPES.get("FUNCTION")) or \
                    (type_2 == Blueprint.TYPES.get("ATTRIBUTE")):
                valid = False
        if type_1 == Blueprint.TYPES.get("SPRITE"):
            if type_2 == Blueprint.TYPES.get("SPRITE"):
                valid = False
        for con in self.__bps_connections:
            if ((con[0] == bp_1) and (con[1] == bp_2)) or \
                    ((con[0] == bp_2) and (con[1] == bp_1)):
                valid = False
        if valid:
            if type_1 == Blueprint.TYPES.get("CHARACTER"):
                if type_2 == Blueprint.TYPES.get("ATTRIBUTE"):
                    bp_1.get_blueprint().add_attribute(bp_2.get_blueprint())
                elif type_2 == Blueprint.TYPES.get("FUNCTION"):
                    bp_1.get_blueprint().add_function(bp_2.get_blueprint())
                elif type_2 == Blueprint.TYPES.get("SPRITE"):
                    bp_1.get_blueprint().add_sprite(bp_2.get_blueprint())
            elif type_1 == Blueprint.TYPES.get("SPRITE"):
                if type_2 == Blueprint.TYPES.get("ATTRIBUTE"):
                    bp_1.get_blueprint().add_attribute(bp_2.get_blueprint())
                elif type_2 == Blueprint.TYPES.get("FUNCTION"):
                    bp_1.get_blueprint().add_function(bp_2.get_blueprint())
                elif type_2 == Blueprint.TYPES.get("CHARACTER"):
                    bp_2.get_blueprint().add_sprite(bp_1.get_blueprint())
            # OTHER WAY AROUND
            elif type_2 == Blueprint.TYPES.get("CHARACTER"):
                if type_1 == Blueprint.TYPES.get("ATTRIBUTE"):
                    bp_2.get_blueprint().add_attribute(bp_1.get_blueprint())
                elif type_1 == Blueprint.TYPES.get("FUNCTION"):
                    bp_2.get_blueprint().add_function(bp_1.get_blueprint())
                elif type_1 == Blueprint.TYPES.get("SPRITE"):
                    bp_2.get_blueprint().add_sprite(bp_1.get_blueprint())
            elif type_2 == Blueprint.TYPES.get("SPRITE"):
                if type_1 == Blueprint.TYPES.get("ATTRIBUTE"):
                    bp_2.get_blueprint().add_attribute(bp_1.get_blueprint())
                elif type_1 == Blueprint.TYPES.get("FUNCTION"):
                    bp_2.get_blueprint().add_function(bp_1.get_blueprint())
                elif type_1 == Blueprint.TYPES.get("CHARACTER"):
                    bp_1.get_blueprint().add_sprite(bp_2.get_blueprint())

    def remove_connection(self, bp_1, bp_2):
        pare = None
        for root, slave in self.__bps_connections:
            if root == bp_1 and slave == bp_2:
                pare = [root, slave]
                break
            elif root == bp_2 and slave == bp_1:
                pare = [root, slave]
                break
        if pare is not None:
            self.__bps_connections.remove(pare)

    def remove_blueprint(self):
        """Description: Method removes focused blueprint and connections associated with it"""
        bp = None
        for temp in self.__bps:
            if temp.focused:
                bp = temp
                break
        # remove connections
        conns = [[root, slave] for root, slave in self.__bps_connections if bp == root or bp == slave]
        for conn in conns:
            self.__bps_connections.remove(conn)
        # finally remove blueprint
        self.__bps.remove(bp)
        # clear character and sprite connections
        for temp in self.__bps:
            root, slave = bp.get_blueprint(), temp.get_blueprint()

            if isinstance(temp, CharacterBlueprint):
                if isinstance(bp, AttributeBlueprint) and (root in slave.attributes):
                    slave.attributes.remove(root)
                elif isinstance(bp, FunctionBlueprint) and (root in slave.functions):
                    slave.functions.remove(root)
                elif isinstance(bp, SpriteBlueprint) and (root in slave.sprites):
                    slave.sprites.remove(root)
            elif isinstance(temp, SpriteBlueprint):
                if isinstance(bp, AttributeBlueprint) and (root in slave.attributes):
                    slave.attributes.remove(root)
                elif isinstance(bp, FunctionBlueprint) and (root in slave.functions):
                    slave.functions.remove(root)
        self.__cont_panel.set_blueprint(None)

    def update_connections(self):
        self.__bps_connections.clear()
        for bp in self.__bps:
            root = bp.get_blueprint()
            if isinstance(bp, CharacterBlueprint):
                if len(root.attributes) > 0:
                    for b in root.attributes:
                        if isinstance(b, AB):
                            self.__bps_connections.append([bp, self.find_blueprint(b)])
                if len(root.functions) > 0:
                    for b in root.functions:
                        if isinstance(b, FB):
                            self.__bps_connections.append([bp, self.find_blueprint(b)])
                if len(root.sprites) > 0:
                    for b in root.sprites:
                        if isinstance(b, SB):
                            self.__bps_connections.append([bp, self.find_blueprint(b)])
            elif isinstance(bp, SpriteBlueprint):
                if len(root.attributes) > 0:
                    for b in root.attributes:
                        if isinstance(b, AB):
                            self.__bps_connections.append([bp, self.find_blueprint(b)])
                if len(root.functions) > 0:
                    for b in root.functions:
                        if isinstance(b, FB):
                            self.__bps_connections.append([bp, self.find_blueprint(b)])

    def find_blueprint(self, blueprint):
        r = None
        for bp in self.__bps:
            if bp.get_blueprint() == blueprint:
                r = bp
        return r

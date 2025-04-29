import struct
import logging
import random
import operator
from typing import List, Literal, Callable
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class Header:
    version_signature: int
    number_of_scripts: int
    number_of_pieces: int
    total_bytes_of_scripts: int
    number_static_vars: int
    always_0: int
    offset_to_script_code_index_array: int
    offset_to_script_name_offset_array: int
    offset_to_piece_name_offset_array: int
    offset_to_script_code: int
    offset_to_name_array: int
    offset_to_sound_array: int
    number_of_sounds: int
    
class InterpreterMeta:
    def __init__(self, header: Header, data: bytes) -> None:
        self.header: Header = header
        self.script_name_offsets: List[int] = []
        self.script_names: List[str] = []
        self.script_offsets: List[int] = []
        
        # script name offsets
        offset = header.offset_to_script_name_offset_array
        indexes = data[offset:offset+header.number_of_scripts*4]
        self.script_name_offsets = list(struct.unpack("l"*header.number_of_scripts, indexes))
        
        # get script names
        self.script_names = [
            get_string(data, offset) for offset in self.script_name_offsets
        ]
        
        # script offsets
        offset = header.offset_to_script_code_index_array
        indexes = data[offset:offset+header.number_of_scripts*4]
        self.script_offsets = [
            header.offset_to_script_code + offset * 4 for offset
            in struct.unpack("l"*header.number_of_scripts, indexes)
        ]
        
        logger.info(self.script_name_offsets)
        logger.info(self.script_names)
        logger.info(self.script_offsets)
        
    def get_script_offset(self, script_name: str) -> int:
        return self.script_offsets[self.script_names.index(script_name)]
        
    
def get_string(data, offset):
    return data[offset:].split(b"\x00")[0].decode("ascii")


# ARMFGUARD uses 69 and 70 (likes them both being > 1)
class System:
    #define ACTIVATION			1	// set or get
    #define STANDINGMOVEORDERS	2	// set or get
    #define STANDINGFIREORDERS	3	// set or get
    #define HEALTH				4	// get (0-100%)
    #define INBUILDSTANCE		5	// set or get
    #define BUSY				6	// set or get (used by misc. special case missions like transport ships)
    #define PIECE_XZ			7	// get
    #define PIECE_Y				8	// get
    #define UNIT_XZ				9	// get
    #define	UNIT_Y				10	// get
    #define UNIT_HEIGHT			11	// get
    #define XZ_ATAN				12	// get atan of packed x,z coords
    #define XZ_HYPOT			13	// get hypot of packed x,z coords
    #define ATAN				14	// get ordinary two-parameter atan
    #define HYPOT				15	// get ordinary two-parameter hypot
    #define GROUND_HEIGHT		16	// get
    #define BUILD_PERCENT_LEFT	17	// get 0 = unit is built and ready, 1-100 = How much is left to build
    #define YARD_OPEN			18	// set or get (change which plots we occupy when building opens and closes)
    #define BUGGER_OFF			19	// set or get (ask other units to clear the area)
    #define ARMORED				20	// set or get
    # "WEAPON_AIM_ABORTED"  	21
    # "WEAPON_READY"			22
    # "WEAPON_LAUNCH_NOW"		23
    # "FINISHED_DYING"		    26
    # "ORIENTATION"			    27
    # "IN_WATER"			    28
    # "CURRENT_SPEED"			29
    # "MAGIC_DEATH"			    31
    # "VETERAN_LEVEL"			32
    # "ON_ROAD"			        34
    #define WEAPON_AIM_ABORTED  21
    #define WEAPON_READY        22
    #define WEAPON_LAUNCH_NOW   23
    #define FINISHED_DYING      26
    #define ORIENTATION         27*/
    #define IN_WATER            28
    #define CURRENT_SPEED       29
    #define MAGIC_DEATH         31
    #define VETERAN_LEVEL       32
    #define ON_ROAD             34

    #define MAX_ID                    70
    #define MY_ID                     71
    #define UNIT_TEAM                 72
    #define UNIT_BUILD_PERCENT_LEFT   73
    #define UNIT_ALLIED               74
    #define MAX_SPEED                 75
    #define CLOAKED                   76
    #define WANT_CLOAK                77
    #define GROUND_WATER_HEIGHT       78 // get land height, negative if below water
    #define UPRIGHT                   79 // set or get
    #define	POW                       80 // get
    #define PRINT                     81 // get, so multiple args can be passed
    #define HEADING                   82 // get
    #define TARGET_ID                 83 // get
    #define LAST_ATTACKER_ID          84 // get
    #define LOS_RADIUS                85 // set or get
    #define AIR_LOS_RADIUS            86 // set or get
    #define RADAR_RADIUS              87 // set or get
    #define JAMMER_RADIUS             88 // set or get
    #define SONAR_RADIUS              89 // set or get
    #define SONAR_JAM_RADIUS          90 // set or get
    #define SEISMIC_RADIUS            91 // set or get
    #define DO_SEISMIC_PING           92 // get
    #define CURRENT_FUEL              93 // set or get
    #define TRANSPORT_ID              94 // get
    #define SHIELD_POWER              95 // set or get
    #define STEALTH                   96 // set or get
    #define CRASHING                  97 // set or get, returns whether aircraft isCrashing state
    #define CHANGE_TARGET             98 // set, the value it's set to determines the affected weapon
    #define CEG_DAMAGE                99 // set
    #define COB_ID                   100 // get
    #define PLAY_SOUND               101 // get, so multiple args can be passed
    #define KILL_UNIT                102 // get KILL_UNIT(unitId, SelfDestruct=true, Reclaimed=false)
    #define SET_WEAPON_UNIT_TARGET   106 // get (fake set)
    #define SET_WEAPON_GROUND_TARGET 107 // get (fake set)
    #define SONAR_STEALTH            108 // set or get
    #define REVERSING                109 // get

    #define FLANK_B_MODE             120 // set or get
    #define FLANK_B_DIR              121 // set or get, set is through get for multiple args
    #define FLANK_B_MOBILITY_ADD     122 // set or get
    #define FLANK_B_MAX_DAMAGE       123 // set or get
    #define FLANK_B_MIN_DAMAGE       124 // set or get
    #define WEAPON_RELOADSTATE       125 // get (with fake set)
    #define WEAPON_RELOADTIME        126 // get (with fake set)
    #define WEAPON_ACCURACY          127 // get (with fake set)
    #define WEAPON_SPRAY             128 // get (with fake set)
    #define WEAPON_RANGE             129 // get (with fake set)
    #define WEAPON_PROJECTILE_SPEED  130 // get (with fake set)
    #define MIN                      131 // get
    #define MAX                      132 // get
    #define ABS                      133 // get
    #define GAME_FRAME               134 // get
    #define KSIN                     135 // get (kiloSine    : 1024*sin(x))
    #define KCOS                     136 // get (kiloCosine  : 1024*cos(x))
    #define KTAN                     137 // get (kiloTangent : 1024*tan(x))
    #define SQRT                     138 // get (square root)
    
    def __init__(self) -> None:       
        self.activated = 1
        self.standing_move_orders = 0
        self.standing_fire_orders = 0
        self.in_build_distance = 0
        self.busy = 0
        self.yard_open = 0
        self.bugger_off = 0
        self.armoured = 0
        
        self.get_port_map = {
            1: lambda: self.activated, 
            2: lambda: self.standing_move_orders,
            3: lambda: self.standing_move_orders, 
            4: lambda: 100,
            5: lambda: self.in_build_distance,
            6: lambda: self.busy,
            7: lambda piece_num, _: 0,
            8: lambda piece_num, _: 0,
            9: lambda unit_num, _: 0,
            10: lambda unit_num, _: 0,
            11: lambda unit_num, _: 0,
            12: lambda xz, _: 0,
            13: lambda xz, _: 0,
            14: lambda a, b: 0,
            15: lambda a, b: 0,
            16: lambda xz, _: 0, 
            17: lambda: 0,
            18: lambda: self.yard_open,
            19: lambda: self.bugger_off,
            20: lambda: self.armoured,
            
            # 69: lambda: 2,
            # 70: lambda: 2,
        }
        
        self.static_vars = {}
        
    def get_static_var(self, var_index: int) -> int:
        return self.static_vars.get(var_index, 0)
        
    def set_static_var(self, var_index: int, value: int) -> int:
        self.static_vars[var_index] = value
    
    def get_port(self, port: int, *vars) -> int:
        try:
            return self.get_port_map[port](*vars)
        except:
            print(f"cant find port {port} {vars}")
            return 2
    
    def set_port(self, port: int, val: int):
        if port == 1: self.activated = val
        elif port == 2: self.standing_move_orders = val
        elif port == 3: self.standing_move_orders = val
        elif port == 5: self.in_build_distance = val
        elif port == 6: self.busy = val
        elif port == 18: self.yard_open = val
        elif port == 19: self.bugger_off = val
        elif port == 20: self.armoured = val
        else: raise NotImplementedError(f"cant set port {port}")
        
        

class Interpreter:    
    def __init__(self, data: bytes, meta: InterpreterMeta, system: System, threads) -> None:
        self.opcode_dict = {
            0x10001000: self.move_piece_with_speed,
            0x10002000: self.turn_piece_with_speed,
            0x10003000: self.start_spin,
            0x10004000: self.stop_spin,
            0x10005000: self.show_piece,
            0x10006000: self.hide_piece,
            0x10007000: self.cache_piece,
            0x10008000: self.dont_cache_piece,
            0x1000A000: self.dont_shadow,
            0x1000B000: self.move_piece_now,
            0x1000C000: self.turn_piece_now,
            0x1000E000: self.dont_shade,
            0x1000F000: self.emit_sfx_from_piece,
            0x10011000: self.wait_for_turn,
            0x10012000: self.wait_for_move,
            0x10013000: self.sleep,
            0x10021001: self.push_constant_to_stack,
            0x10021002: self.push_local_to_stack,
            0x10021004: self.push_static_to_stack,
            0x10022000: self.locals_allocate,
            0x10023002: self.set_local_var,
            0x10023004: self.set_static_var,
            0x10024000: self.pop_stack,
            0x10031000: self.binary_op(operator.add),
            0x10032000: self.binary_op(operator.sub),
            0x10033000: self.binary_op(operator.mul),
            0x10034000: self.binary_op(operator.floordiv),
            0x10035000: self.binary_op(operator.and_), # bitwise and
            0x10036000: self.binary_op(operator.or_), # bitwise or
            0x10039000: self.binary_op(operator.add), # unknown 1
            0x1003A000: self.binary_op(operator.add), # unknown 2
            0x1003B000: self.binary_op(operator.add), # unknown 3
            0x10041000: self.binary_op(random.randint),
            0x10042000: self.get_unit_value,
            0x10043000: self.get_function_result, # dont know what this does but we will find out some day!
            0x10051000: self.binary_op(operator.lt),
            0x10052000: self.binary_op(operator.le),
            0x10053000: self.binary_op(operator.gt),
            0x10054000: self.binary_op(operator.ge),
            0x10055000: self.binary_op(operator.eq),
            0x10056000: self.binary_op(operator.ne),
            0x10057000: self.binary_op(lambda l, r: l and r), # boolean and
            0x10058000: self.binary_op(lambda l, r: l or r), # boolean or
            0x1005A000: self.not_,
            0x10061000: self.start_script,
            0x10062000: self.call_script,
            0x10064000: self.jump_to_offset,
            0x10065000: self.return_,
            0x10066000: self.jump_if_false, 
            0x10067000: self.signal,
            0x10068000: self.set_signal_mask,
            0x10071000: self.explode_piece,
            0x10072000: self.play_sound,
            0x10073000: self.map_command,
            0x10082000: self.set_unit_value,
            0x10083000: self.attach_unit,
            0x10084000: self.drop_unit,
        }
        self.state: Literal["running", "sleeping", "idle"] = "running" # running, sleeping, idle
        self.system: System = system
        self.meta: InterpreterMeta = meta
        self.header: Header = meta.header
        self.data: bytes = data
        self.script: str = None
        self.sleep_duration: int = 0
        self.cursor: int = 0
        self.signal_mask: int = 0
        self.killed: bool = False
        self.stack: List[int] = []
        self.local_vars: List[int] = []
        self.return_to: List[int] = []
        self.threads: List[Interpreter] = threads
        
    def check_signal(self, signal) -> bool:
        return self.signal_mask == signal

    def next(self) -> None:
        self.cursor += 4

    def get_long(self) -> int:
        return struct.unpack("l", self.data[self.cursor:self.cursor+4])[0]
    
    def binary_op(self, operator: Callable[[int, int], int]) -> Callable:
        def executor():
            right = self.stack.pop()
            left = self.stack.pop()
            ans = operator(left, right)
            self.stack.append(ans)
            logger.info(f"binary_op called op: {left} {operator} {right} = {ans}")
        return executor
    
    ###### instructions
    
    # 0x10002000
    def move_piece_with_speed(self):
        self.stack.pop() # dest
        self.stack.pop() # speed
        self.next() # piece
        self.next() # axis
        logger.info("move_piece_with_speed called (dont care)")
    
    # 0x10001000
    def turn_piece_with_speed(self):
        self.stack.pop() # dest
        self.stack.pop() # speed
        self.next() # piece
        self.next() # axis
        logger.info("turn_piece_with_speed called (dont care)")
        
    # 0x10003000
    def start_spin(self):
        self.stack.pop() # deccel
        self.stack.pop() # accel
        self.next() # piece
        self.next() # axis
        logger.info("start_spin called (dont care)")
        
    # 0x10004000
    def stop_spin(self):
        self.stack.pop() # deccel
        self.next() # piece
        self.next() # axis
        logger.info("stop_spin called (dont care)")
    
    # 0x10005000
    def show_piece(self):
        self.next() # piece
        logger.info("show_piece called (dont care)")
        
    # 0x10006000
    def hide_piece(self):
        self.next() # piece
        logger.info(f"hide_piece called (dont care)")
        
    # 0x10007000
    def cache_piece(self):
        self.next() # piece
        logger.info(f"cache_piece called (dont care)")
    
    # 0x10008000
    def dont_cache_piece(self):
        self.next() # piece
        logger.info("dont_cache_piece called (dont care)")
    
    # 0x1000A000 
    def dont_shadow(self):
        self.next() # piece
        logger.info("dont_shadow called (dont care)")
    
    # 0x1000B000
    def move_piece_now(self):
        self.stack.pop() # position
        self.next() # piece
        self.next() # axis
        logger.info("move_piece_now (dont care)")
    
    # 0x1000C000
    def turn_piece_now(self):
        self.stack.pop() # angle
        self.next() # piece
        self.next() # axis
        logger.info("turn_piece_now (dont care)")
    
    # 0x1000E000
    def dont_shade(self):
        self.next() # piece
        logger.info("dont_shade called (dont care)")
    
    # 0x1000F000
    def emit_sfx_from_piece(self):
        self.stack.pop() # sfx
        self.next() # piece
        logger.info("emit_sfx_from_piece called (dont care)")
        
    # 0x10011000
    def wait_for_turn(self):
        self.next() # piece
        self.next() # axis
        logger.info("wait_for_turn called (dont care)")
        
    # 0x10012000
    def wait_for_move(self):
        self.next() # piece
        self.next() # axis
        logger.info("wait_for_move called (dont care)")

    # 0x10013000 
    def sleep(self):
        self.sleep_duration = self.stack.pop()
        self.state = "sleeping"
        logger.info(f"sleeping for {self.sleep_duration}ms")

    # 0x10021001
    def push_constant_to_stack(self):
        constant = self.get_long()
        self.next()
        self.stack.append(constant)
        logger.info(f"push_constant_to_stack: {constant}")
        
    # 0x10021002 
    def push_local_to_stack(self):
        var_index = self.get_long()
        self.next()
        val = self.local_vars[var_index]
        self.stack.append(val)
        logger.info(f"push_local_to_stack idx: {var_index}, val: {val}")
    
    # 0x10021004
    def push_static_to_stack(self):
        static_var_index = self.get_long()
        self.next()
        val = self.system.get_static_var(static_var_index)
        self.stack.append(val)
        logger.info(f"push_static_to_stack idx: {static_var_index}, val: {val}")

    # 0x10022000 
    def locals_allocate(self):
        self.local_vars.append(0)
        logger.info("stack_allocate")

    # 0x10023002 
    def set_local_var(self):
        var_index = self.get_long()
        self.next()
        val = self.stack.pop()
        self.local_vars[var_index] = val
        logger.info(f"set_local idx: {var_index}, val: {val}")

    # 0x10023004 
    def set_static_var(self):
        static_var_index = self.get_long()
        self.next()
        val = self.stack.pop()
        self.system.set_static_var(static_var_index, val)
        logger.info(f"set_static_var idx: {static_var_index}, val: {val}")
        
    # 0x10024000
    def pop_stack(self):
        self.stack.pop()
        logger.info("pop_stack")
    
    # 0x10042000   
    def get_unit_value(self):
        port = self.stack.pop()
        val = self.system.get_port(port)
        self.stack.append(val)
        logger.info(f"get_unit_value {val} from port {port}")
        
    # 0x10043000
    def get_function_result(self):
        self.stack.pop() # unused 4th var
        self.stack.pop() # unused 3rd var
        right = self.stack.pop() # 2nd var
        left = self.stack.pop() # 1st var
        port = self.stack.pop() # port
        ans = self.system.get_port(port, left, right)
        self.stack.append(ans)
        logger.info(f"get_function_result {port} {left} {right} {ans}")
    
    # 0x1005A000 
    def not_(self):
        old_val = self.stack.pop()
        new_val = not old_val
        self.stack.append(new_val)
        logger.info(f"not_ {old_val} to {new_val}")
        
    # 0x10061000
    def start_script(self):
        # starts a new function in parallel with the current function
        script_index = self.get_long()
        self.next()
        num_params = self.get_long()
        self.next()
        
        if self.meta.script_names[script_index] not in ("SmokeUnit", "PositionLegs", "LegGroups"):
            interpreter = Interpreter(self.data, self.meta, self.system, self.threads)
            interpreter.load_script(
                self.meta.script_names[script_index],
                self.stack[0:num_params]
            )
            interpreter.signal_mask = self.signal_mask
            self.threads.append(interpreter)
            logger.info(f"start_script called on script {script_index} {self.meta.script_names[script_index]}")
            
        self.stack = []
        
    # 0x10062000
    def call_script(self):
        # noraml function call, does function then returns back
        script_index = self.get_long()
        self.next() 
        self.next() # params
        
        self.return_to.append(self.cursor)
        script_name = self.meta.script_names[script_index]
        self.script = script_name
        self.cursor = self.meta.get_script_offset(script_name)
        
        logger.info(f"call_script called on script {script_index} {script_name}")
        
    # 0x10064000 
    def jump_to_offset(self):
        offset = self.get_long()
        self.next()
        self.cursor = self.header.offset_to_script_code + offset * 4 
        logger.info(f"jump_to_offset {self.cursor}")

    # 0x10065000
    def return_(self):
        val = self.stack.pop()
        logger.info(f"function returned {val}")
        return val
    
    # 0x10066000 
    def jump_if_false(self):
        val = self.stack.pop()
        offset = self.get_long()
        self.next()
        if val == 0:
            offset = self.header.offset_to_script_code + offset * 4 
            self.cursor = offset
        logger.info(f"jump_if_false {val}")
        
    # 0x10067000
    def signal(self):
        signal = self.stack.pop()
        
        # stop other interpreters that have this signal mask!
        for t in self.threads:
            if t.signal_mask == signal and t != self:
                t.killed = True
                t.state = "idle"
                self.threads.remove(t)
            
        logger.info(f"signal {signal} called")
        
    # 0x10068000 
    def set_signal_mask(self):
        self.signal_mask = self.stack.pop()
        logger.info(f"set_signal_mask to {self.signal_mask}")
        
    # 0x10071000
    def explode_piece(self):
        self.stack.pop() # type
        self.next() # piece
        logger.info("explode_piece called (dont care)")
        
    # 0x10072000
    def play_sound(self):
        self.next() # sfx
        logger.info("play_sound called (dont care)")
        
    # 0x10073000
    def map_command(self):
        self.next() # something
        self.next() # something
        logger.info("map_command called (dont care)")

    # 0x10082000 
    def set_unit_value(self):
        val = self.stack.pop()
        port = self.stack.pop()
        self.system.set_port(port, val)
        logger.info(f"set_unit_value called {port} set to {val}")

    # 0x10083000 
    def attach_unit(self):
        self.stack.pop() 
        self.stack.pop() 
        self.stack.pop() 
        logger.info("attach_unit called (dont care)")
        
    # 0x10084000 
    def drop_unit(self):
        self.stack.pop()
        logger.info("drop_unit called (dont care)")

    #### the other stuff    
        
    def do_command(self) -> int | None:
        opcode = self.get_long()
        self.next()
        
        if opcode in self.opcode_dict:
            return self.opcode_dict[opcode]()
        else:
            raise Exception(f"opcode {opcode} not found in opcode dict")
        
    def run(self) -> int:
        if self.sleep_duration is not None and self.sleep_duration > 0:
            self.state = "sleeping"
            return None
        
        if self.killed:
            logger.info("KILLED!!")
            self.state = "idle"
            return None
        
        self.state = "running"
        logger.info(f"run function {self.script}")
        return_val = None
    
        while return_val is None:
            return_val = self.do_command()
            if self.state == "sleeping":
                return None

            if return_val is not None and len(self.return_to) > 0:
                self.cursor = self.return_to.pop()
                self.stack = []
                self.return_val = None
        
        self.state = "idle"
        if self in self.threads: self.threads.remove(self)
        return return_val
    
    def load_script(self, script_name: str, local_vars: List[int]):
        logger.info(f"LOADED SCRIPT {script_name}")
        self.script = script_name
        self.cursor = self.meta.get_script_offset(script_name)
        self.stack = []
        self.local_vars = local_vars
        self.state = "running"
        self.killed = False
        self.signal_mask = None
        




def calculate_reload_speed(script_bytes: bytes, weapon: str, min_reload: int, in_water: bool) -> float | None:
    if weapon.lower() == "primary":
        aim_script = "AimPrimary"
        query_script = "QueryPrimary"
        fire_script = "FirePrimary"
    elif weapon.lower() == "secondary":
        aim_script = "AimSecondary"
        query_script = "QuerySecondary"
        fire_script = "FireSecondary"
    elif weapon.lower() == "tertiary":
        aim_script = "AimTertiary"
        query_script = "QueryTertiary"
        fire_script = "FireTertiary"
        
    header = Header(*struct.unpack("l"*13, script_bytes[:4*13]))
    logger.info(header)
    meta = InterpreterMeta(header, script_bytes)
        
    if query_script not in meta.script_names:
        return None
    
    # interpret it
    system = System()
    global_time: int = 0 
    amount_fired: int = 0
    threads: List[Interpreter] = []
    interpreter = Interpreter(script_bytes, meta, system, threads)
    threads.append(interpreter)
    interpreter.load_script("Create", [])
    interpreter.run()
        
    if in_water and "setSFXoccupy" in meta.script_names:
        # water weapons need to have this done for them to work!
        moves = Interpreter(script_bytes, meta, system, threads)
        threads.append(moves)
        moves.load_script("setSFXoccupy", [2])
        moves.run()
        
        if "StartMoving" in meta.script_names:
            s = Interpreter(script_bytes, meta, system, threads)
            threads.append(s)
            s.load_script("StartMoving", [])
            s.run()

        if "StopMoving" in meta.script_names:
            s = Interpreter(script_bytes, meta, system, threads)
            threads.append(s)
            s.load_script("StopMoving", [])
            s.run()


    # interpreter.sleep_duration = 0
    reload_time = max(min_reload, 33)
    next_fire: int = 0
    
    action: Literal["aim", "fire", None] = "aim" if aim_script in meta.script_names else "fire"
    # can fire if AimWeapon reutrn 1 and reloaded
    can_aim = aim_script in meta.script_names
    
    if can_aim:
        aim = True
        aimed = False
        reloaded = True
        
        while True:
            
            if aim or True:
                # print("start aim")
                # do action
                s = Interpreter(script_bytes, meta, system, threads)
                s.load_script(aim_script, [0, 0])
                threads.append(s)
                aim = False
                
            if aimed and reloaded:
                # print("fire")
                # query (actual firing)
                s1 = Interpreter(script_bytes, meta, system, threads)
                s1.load_script(query_script, [0])
                threads.append(s1)
                
                # run animation
                if fire_script in meta.script_names:
                    s2 = Interpreter(script_bytes, meta, system, threads)
                    s2.load_script(fire_script, [])
                    threads.append(s2)
                    
                next_fire = global_time + reload_time
                reloaded = False
                aimed = False
                
                amount_fired += 1
                if amount_fired == 10:
                    return global_time/9
            
            
            # run scripts
            for s in threads:
                temp_ret = s.run()
                if s.script == aim_script and temp_ret == 1:
                    aimed = True
                # if s.script == fire_script and s.state == "idle":
                    # aim = True
            
            # increment time
            sleeps = [s.sleep_duration for s in threads if s.state == "sleeping"]
            if next_fire - global_time > 0:
                sleeps.append(next_fire - global_time)
            min_sleep = min(sleeps or [0])
            global_time += min_sleep
            
            for script in threads:
                script.sleep_duration -= min_sleep
                
            logger.info(global_time)
            
            if next_fire <= global_time:
                reloaded = True
                # aim = True
        
        
    else:
        reloaded = True
        
        while True:
            if reloaded:
                # query (actual firing)
                s1 = Interpreter(script_bytes, meta, system, threads)
                s1.load_script(query_script, [0])
                threads.append(s1)
                
                # run animation
                if fire_script in meta.script_names:
                    s2 = Interpreter(script_bytes, meta, system, threads)
                    s2.load_script(fire_script, [])
                    threads.append(s2)
                    
                next_fire = global_time + reload_time
                reloaded = False
                
                amount_fired += 1
                if amount_fired == 10:
                    return global_time/9
            
            # run scripts
            for s in threads:
                s.run()
            
            # increment time
            sleeps = [s.sleep_duration for s in threads if s.state == "sleeping"]
            if next_fire - global_time > 0:
                sleeps.append(next_fire - global_time)
            min_sleep = min([s for s in sleeps if s != 0] or [0])
            global_time += min_sleep
            
            for script in threads:
                script.sleep_duration -= min_sleep
                
            logger.info(global_time)
            
            if next_fire <= global_time:
                reloaded = True



if __name__ == "__main__":
    def do_all():
        import os
        directory = "out/scripts/"
        for f in os.listdir(directory):
            if f.lower().endswith(".cob"):
                with open(f"{directory}{f}", mode="rb") as file:
                    data = file.read()

                    try:
                        reload_speed = calculate_reload_speed(data, "primary", 400)
                        if reload_speed is not None:
                            print(f"{f} Reload speed: {reload_speed}ms")
                    except:
                        print(f"no reload speed for {f}")
                    
    def do(unit_name, weapon, rs, water):
        # logging.basicConfig(level=logging.INFO, format=('%(filename)s: '    
        #                         '%(levelname)s: '
        #                         '%(funcName)s(): '
        #                         '%(lineno)d:\t'
        #                         '%(message)s')
        #                 )
        
        with open(f"{unit_name}", mode="rb") as file:
            data = file.read()

            reload_speed = calculate_reload_speed(data, weapon, rs, water)
            print(f"{unit_name} Reload speed: {reload_speed}ms")

    # do_all()
    do("extracted_files/t3esc/scripts/ARMASPID.cob", "primary", 400, False)
    


# setSFXoccupy(terrainType)
# 0 = none
# 1/2 = water
# 3 = ???
# 4 = land
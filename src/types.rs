use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Clone, Debug, PartialEq)]
pub struct EscDataCtx {
    pub meta: Meta,
    pub units: HashMap<String, Unit>,
    pub weapons: HashMap<String, Weapon>,
}

#[derive(Default, Serialize, Deserialize, Debug, Clone, PartialEq)]
#[serde(default)]
pub struct Meta {
    pub updated_at: i64,
}

#[derive(Default, Serialize, Deserialize, Debug, Clone, PartialEq)]
#[serde(default)]
pub struct Unit {
    #[serde(rename = "acceleration")]
    pub acceleration: f64,
    #[serde(rename = "activatewhenbuilt")]
    pub activate_when_built: i64,
    #[serde(rename = "ai_limit")]
    pub ai_limit: String,
    #[serde(rename = "ai_weight")]
    pub ai_weight: String,
    #[serde(rename = "altfromsealevel")]
    pub alt_from_sea_level: i64,
    #[serde(rename = "amphibious")]
    pub amphibious: i64,
    #[serde(rename = "antiweapons")]
    pub anti_weapons: i64,
    #[serde(rename = "attackrunlength")]
    pub attack_run_length: i64,
    #[serde(rename = "badtargetcategory")]
    pub bad_target_category: String,
    #[serde(rename = "bankscale")]
    pub bank_scale: f64,
    #[serde(rename = "bmcode")]
    pub bm_code: i64,
    #[serde(rename = "brakerate")]
    pub brake_rate: f64,
    #[serde(rename = "buildangle")]
    pub build_angle: i64,
    #[serde(rename = "buildcostenergy")]
    pub build_cost_energy: i64,
    #[serde(rename = "buildcostmetal")]
    pub build_cost_metal: i64,
    #[serde(rename = "builddistance")]
    pub build_distance: i64,
    #[serde(rename = "builder")]
    pub builder: i64,
    #[serde(rename = "buildtime")]
    pub build_time: i64,
    #[serde(rename = "canattack")]
    pub can_attack: i64,
    #[serde(rename = "canbuild")]
    pub can_build: i64,
    #[serde(rename = "cancapture")]
    pub can_capture: i64,
    #[serde(rename = "candgun")]
    pub can_dgun: i64,
    #[serde(rename = "canfly")]
    pub can_fly: i64,
    #[serde(rename = "canguard")]
    pub can_guard: i64,
    #[serde(rename = "canhover")]
    pub can_hover: i64,
    #[serde(rename = "canland")]
    pub can_land: i64,
    #[serde(rename = "canload")]
    pub can_load: i64,
    #[serde(rename = "canmove")]
    pub can_move: i64,
    #[serde(rename = "canpatrol")]
    pub can_patrol: i64,
    #[serde(rename = "canreclamate")]
    pub can_reclamate: i64,
    #[serde(rename = "canrepair")]
    pub can_repair: i64,
    #[serde(rename = "canresurrect")]
    pub can_resurrect: i64,
    #[serde(rename = "canstop")]
    pub can_stop: i64,
    #[serde(rename = "cantbetransported")]
    pub cant_be_transported: i64,
    #[serde(rename = "category")]
    pub category: Vec<String>,
    #[serde(rename = "cloakcost")]
    pub cloak_cost: i64,
    #[serde(rename = "cloakcostmoving")]
    pub cloak_cost_moving: i64,
    #[serde(rename = "commander")]
    pub commander: i64,
    #[serde(rename = "cruisealt")]
    pub cruise_alt: i64,
    #[serde(rename = "damagemodifier")]
    pub damage_modifier: f64,
    #[serde(rename = "defaultmissiontype")]
    pub default_mission_type: String,
    #[serde(rename = "description")]
    pub description: String,
    #[serde(rename = "designation")]
    pub designation: String,
    #[serde(rename = "digger")]
    pub digger: i64,
    #[serde(rename = "downloadable")]
    pub downloadable: i64,
    #[serde(rename = "energymake")]
    pub energy_make: f64,
    #[serde(rename = "energystorage")]
    pub energy_storage: i64,
    #[serde(rename = "energyuse")]
    pub energy_use: f64,
    #[serde(rename = "explodeas")]
    pub explode_as: String,
    #[serde(rename = "extractsmetal")]
    pub extracts_metal: f64,
    #[serde(rename = "firestandorders")]
    pub fire_stand_orders: i64,
    #[serde(rename = "floater")]
    pub floater: i64,
    #[serde(rename = "footprintx")]
    pub footprint_x: i64,
    #[serde(rename = "footprintz")]
    pub footprint_z: i64,
    #[serde(rename = "frenchdescription")]
    pub french_description: String,
    #[serde(rename = "frenchname")]
    pub french_name: String,
    #[serde(rename = "germandescription")]
    pub german_description: String,
    #[serde(rename = "germanname")]
    pub german_name: String,
    #[serde(rename = "healtime")]
    pub heal_time: i64,
    #[serde(rename = "hidedamage")]
    pub hide_damage: i64,
    #[serde(rename = "hoverattack")]
    pub hover_attack: i64,
    #[serde(rename = "immunetoparalyzer")]
    pub immune_to_paralyzer: i64,
    #[serde(rename = "init_cloaked")]
    pub init_cloaked: i64,
    #[serde(rename = "isairbase")]
    pub is_airbase: i64,
    #[serde(rename = "isfeature")]
    pub is_feature: i64,
    #[serde(rename = "istargetingupgrade")]
    pub is_targeting_upgrade: i64,
    #[serde(rename = "italiandescription")]
    pub italian_description: String,
    #[serde(rename = "italianname")]
    pub italian_name: String,
    #[serde(rename = "japanesename")]
    pub japanese_name: String,
    #[serde(rename = "kamikaze")]
    pub kamikaze: i64,
    #[serde(rename = "kamikazedistance")]
    pub kamikaze_distance: i64,
    #[serde(rename = "makesmetal")]
    pub makes_metal: i64,
    #[serde(rename = "maneuverleashlength")]
    pub maneuver_leash_length: i64,
    #[serde(rename = "maxdamage")]
    pub max_damage: i64,
    #[serde(rename = "maxslope")]
    pub max_slope: i64,
    #[serde(rename = "maxvelocity")]
    pub max_velocity: f64,
    #[serde(rename = "maxwaterdepth")]
    pub max_water_depth: i64,
    #[serde(rename = "metalmake")]
    pub metal_make: f64,
    #[serde(rename = "metalstorage")]
    pub metal_storage: i64,
    #[serde(rename = "mincloakdistance")]
    pub min_cloak_distance: i64,
    #[serde(rename = "minwaterdepth")]
    pub min_water_depth: i64,
    #[serde(rename = "mobilestandorders")]
    pub mobile_stand_orders: i64,
    #[serde(rename = "movementclass")]
    pub movement_class: String,
    #[serde(rename = "moverate1")]
    pub move_rate_1: i64,
    #[serde(rename = "name")]
    pub name: String,
    #[serde(rename = "noautofire")]
    pub no_auto_fire: i64,
    #[serde(rename = "nochasecategory")]
    pub no_chase_category: String,
    #[serde(rename = "norestrict")]
    pub no_restrict: i64,
    #[serde(rename = "noshadow")]
    pub no_shadow: i64,
    #[serde(rename = "objectname")]
    pub object_name: String,
    #[serde(rename = "onoffable")]
    pub on_off_able: i64,
    #[serde(rename = "ovradjust")]
    pub ovr_adjust: i64,
    #[serde(rename = "piglatindescription")]
    pub pig_latin_description: String,
    #[serde(rename = "piglatinname")]
    pub pig_latin_name: String,
    #[serde(rename = "pitchscale")]
    pub pitch_scale: f64,
    #[serde(rename = "radardistance")]
    pub radar_distance: i64,
    #[serde(rename = "radardistancejam")]
    pub radar_distance_jam: i64,
    #[serde(rename = "resurrect")]
    pub resurrect: i64,
    #[serde(rename = "rof1")]
    pub rof_1: f64,
    #[serde(rename = "rof3")]
    pub rof_3: f64,
    #[serde(rename = "scale", alias = "sscale")]
    pub scale: f64,
    #[serde(rename = "selfdestructas")]
    pub self_destruct_as: String,
    #[serde(rename = "selfdestructcountdown")]
    pub self_destruct_countdown: i64,
    #[serde(rename = "shootme")]
    pub shoot_me: i64,
    #[serde(rename = "showplayername")]
    pub show_player_name: i64,
    #[serde(rename = "side")]
    pub side: String,
    #[serde(rename = "sightdistance")]
    pub sight_distance: i64,
    #[serde(rename = "sonardistance")]
    pub sonar_distance: i64,
    #[serde(rename = "sonardistancejam")]
    pub sonar_distance_jam: i64,
    #[serde(rename = "sortbias")]
    pub sort_bias: i64,
    #[serde(rename = "soundcategory")]
    pub sound_category: String,
    #[serde(rename = "spanishdescription")]
    pub spanish_description: String,
    #[serde(rename = "spanishname")]
    pub spanish_name: String,
    #[serde(rename = "standingfireorder")]
    pub standing_fire_order: i64,
    #[serde(rename = "standingmoveorder")]
    pub standing_move_order: i64,
    #[serde(rename = "stealth")]
    pub stealth: i64,
    #[serde(rename = "steeringmode")]
    pub steering_mode: i64,
    #[serde(rename = "tedclass")]
    pub ted_class: String,
    #[serde(rename = "threed")]
    pub threed: i64,
    #[serde(rename = "tidalgenerator")]
    pub tidal_generator: i64,
    #[serde(rename = "transportcapacity")]
    pub transport_capacity: i64,
    #[serde(rename = "transportmaxunits")]
    pub transport_max_units: i64,
    #[serde(rename = "transportsize")]
    pub transport_size: i64,
    #[serde(rename = "turnrate")]
    pub turn_rate: i64,
    #[serde(rename = "unitname")]
    pub unit_name: String,
    #[serde(rename = "unitnumber")]
    pub unit_number: i64,
    #[serde(rename = "upright")]
    pub upright: i64,
    #[serde(rename = "waterline")]
    pub water_line: f64,
    #[serde(rename = "weapon1")]
    pub weapon_1: Option<String>,
    #[serde(rename = "weapon2")]
    pub weapon_2: Option<String>,
    #[serde(rename = "weapon3")]
    pub weapon_3: Option<String>,
    #[serde(rename = "windgenerator")]
    pub wind_generator: i64,
    #[serde(rename = "workertime")]
    pub worker_time: i64,
    #[serde(rename = "wpri_badtargetcategory")]
    pub wpri_bad_target_category: String,
    #[serde(rename = "wsec_badtargetcategory")]
    pub wsec_bad_target_category: String,
    #[serde(rename = "wspe_badtargetcategory")]
    pub wspe_bad_target_category: String,
    #[serde(rename = "yardmap")]
    pub yar_dmap: Vec<String>,
    #[serde(rename = "zbuffer")]
    pub z_buffer: i64,
    #[serde(rename = "builtby")]
    pub built_by: Vec<String>,
    #[serde(rename = "builds")]
    pub builds: Vec<String>,
    #[serde(rename = "tier")]
    pub tier: i64,
    #[serde(rename = "roviclass")]
    pub rovi_class: String,
}

#[derive(Default, Serialize, Deserialize, Debug, Clone, PartialEq)]
#[serde(default)]
pub struct Weapon {
    #[serde(rename = "accuracy")]
    pub accuracy: i64,
    #[serde(rename = "aimrate")]
    pub aim_rate: i64,
    #[serde(rename = "areaofeffect")]
    pub area_of_effect: i64,
    #[serde(rename = "ballistic")]
    pub ballistic: i64,
    #[serde(rename = "beamweapon")]
    pub beam_weapon: i64,
    #[serde(rename = "burnblow")]
    pub burn_blow: i64,
    #[serde(rename = "burst")]
    pub burst: i64,
    #[serde(rename = "burstrate")]
    pub burst_rate: f64,
    #[serde(rename = "color")]
    pub color: i64,
    #[serde(rename = "color2")]
    pub color_2: i64,
    #[serde(rename = "commandfire")]
    pub command_fire: i64,
    #[serde(rename = "coverage")]
    pub coverage: i64,
    #[serde(rename = "cruise")]
    pub cruise: i64,
    #[serde(rename = "damage")]
    pub damage: HashMap<String, i64>,
    #[serde(rename = "dropped")]
    pub dropped: i64,
    #[serde(rename = "duration")]
    pub duration: f64,
    #[serde(rename = "edgeeffectiveness")]
    pub edge_effectiveness: f64,
    #[serde(rename = "endsmoke")]
    pub end_smoke: i64,
    #[serde(rename = "energypershot")]
    pub energy_per_shot: i64,
    #[serde(rename = "explosionart")]
    pub explosion_art: String,
    #[serde(rename = "explosiongaf")]
    pub explosion_gaf: String,
    #[serde(rename = "firestarter")]
    pub fire_starter: i64,
    #[serde(rename = "flighttime")]
    pub flight_time: f64,
    #[serde(rename = "groundbounce")]
    pub ground_bounce: i64,
    #[serde(rename = "guidance")]
    pub guidance: i64,
    #[serde(rename = "holdtime")]
    pub hold_time: i64,
    #[serde(rename = "id")]
    pub id: i64,
    #[serde(rename = "interceptor")]
    pub interceptor: i64,
    #[serde(rename = "lavaexplosionart")]
    pub lava_explosion_art: String,
    #[serde(rename = "lavaexplosiongaf")]
    pub lava_explosion_gaf: String,
    #[serde(rename = "lineofsight")]
    pub line_of_sight: i64,
    #[serde(rename = "metalpershot")]
    pub metal_per_shot: i64,
    #[serde(rename = "meteor")]
    pub meteor: i64,
    #[serde(rename = "minbarrelangle")]
    pub min_barrel_angle: i64,
    #[serde(rename = "model")]
    pub model: String,
    #[serde(rename = "name")]
    pub name: String,
    #[serde(rename = "noautorange")]
    pub no_auto_range: i64,
    #[serde(rename = "noexplode")]
    pub no_explode: i64,
    #[serde(rename = "noradar")]
    pub no_radar: i64,
    #[serde(rename = "paralyzer")]
    pub paralyzer: i64,
    #[serde(rename = "pitchtolerance")]
    pub pitch_tolerance: i64,
    #[serde(rename = "propeller")]
    pub propeller: i64,
    #[serde(rename = "randomdecay")]
    pub random_decay: f64,
    #[serde(rename = "range")]
    pub range: i64,
    #[serde(rename = "reloadtime")]
    pub reload_time: f64,
    #[serde(rename = "rendertype")]
    pub render_type: i64,
    #[serde(rename = "selfprop")]
    pub self_prop: i64,
    #[serde(rename = "shakeduration")]
    pub shake_duration: f64,
    #[serde(rename = "shakemagnitude")]
    pub shake_magnitude: f64,
    #[serde(rename = "smokedelay")]
    pub smoke_delay: f64,
    #[serde(rename = "smoketrail")]
    pub smoke_trail: f64,
    #[serde(rename = "soundtrigger")]
    pub sound_trigger: i64,
    #[serde(rename = "soundwater")]
    pub sound_water: String,
    #[serde(rename = "sprayangle")]
    pub spray_angle: i64,
    #[serde(rename = "startsmoke")]
    pub start_smoke: i64,
    #[serde(rename = "startvelocity")]
    pub start_velocity: i64,
    #[serde(rename = "stockpile")]
    pub stock_pile: i64,
    #[serde(rename = "targetable")]
    pub targetable: i64,
    #[serde(rename = "toairweapon")]
    pub to_air_weapon: i64,
    #[serde(rename = "tolerance")]
    pub tolerance: i64,
    #[serde(rename = "tracks")]
    pub tracks: i64,
    #[serde(rename = "turnrate")]
    pub turn_rate: i64,
    #[serde(rename = "turret")]
    pub turret: i64,
    #[serde(rename = "twophase")]
    pub two_phase: i64,
    #[serde(rename = "unitsonly")]
    pub units_only: i64,
    #[serde(rename = "vlaunch")]
    pub vlaunch: i64,
    #[serde(rename = "waterexplosionart")]
    pub water_explosion_art: String,
    #[serde(rename = "waterexplosiongaf")]
    pub water_explosion_gaf: String,
    #[serde(rename = "waterweapon")]
    pub water_weapon: i64,
    #[serde(rename = "weaponacceleration")]
    pub weapon_acceleration: i64,
    #[serde(rename = "weapontimer")]
    pub weapon_timer: f64,
    #[serde(rename = "weaponvelocity")]
    pub weapon_velocity: i64,
}

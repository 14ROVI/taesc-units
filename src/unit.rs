use crate::app::{set_title, Route};
use crate::types::{EscDataCtx, Unit, Weapon};
use js_sys::JsString;
use js_sys::Number;
use yew::prelude::*;
use yew::Properties;
use yew_router::prelude::*;

fn format_i64(number: i64) -> JsString {
    Number::from(number as i32).to_locale_string("en-GB")
}
fn format_f64(number: f64) -> JsString {
    Number::from(number as f32).to_locale_string("en-GB")
}

#[derive(Properties, PartialEq)]
pub struct UnitPageProps {
    pub unit_name: String,
}

#[function_component(UnitPage)]
pub fn unit_page(props: &UnitPageProps) -> Html {
    let esc_data = use_context::<EscDataCtx>().expect("no ctx found");
    let units = esc_data.units.clone();
    let weapons = esc_data.weapons.clone();
    let unit = units.get(&props.unit_name.clone());

    if let Some(unit) = unit {
        set_title(format!("TA:ESC Units | {}", unit.name).as_str());

        let img_url = format!("/data/unit_icons/{}.webp", unit.object_name.clone());

        html! {
            <>
                <div class="unit-info">
                    <div>
                        <h1>{"("}{ unit.side.clone() }{") "}{ unit.name.clone() }</h1>
                        <p>{ unit.description.clone() }</p>
                        <img width=200 height=200 src={img_url}/>
                        <p>{ "Summon with: "}<code>{ "+" }{ unit.unit_name.clone() }</code></p>
                    </div>
                    <div>
                        <p>{ format!("Costs {} metal", format_i64(unit.build_cost_metal)) }</p>
                        <p>{ format!("Costs {} energy", format_i64(unit.build_cost_energy)) }</p>
                        if unit.energy_make != 0.0 {
                            <p>{ format!("Energy make: {}", format_f64(unit.energy_make)) }</p>
                        }
                        <p>{ format!("Build time: {}", format_i64(unit.build_time)) }</p>
                        <p>{ format!("Health: {}", format_i64(unit.max_damage)) }</p>
                        if unit.damage_modifier != 0.0 {
                            <p>{ format!("Effective health (when armoured): {}", format_f64(unit.max_damage as f64 / unit.damage_modifier)) }</p>
                            <p>{ format!("Armour damage modifier: {}", format_f64(unit.damage_modifier)) }</p>
                        }
                        <p>{ format!("Footprint: {} by {}", unit.footprint_x, unit.footprint_z) }</p>
                        <p>{ format!("Sight distance: {}", unit.sight_distance) }</p>
                        <p>{ format!("Radar distance: {}", unit.radar_distance) }</p>
                        <p>{ format!("Radar Jam distance: {}", unit.radar_distance_jam) }</p>
                        if unit.worker_time > 0 {
                            <p>{ format!("Build power: {}", unit.worker_time) }</p>
                        }
                        if unit.max_slope > 0 {
                            <p>{ format!("Max slope: {}", unit.max_slope) }</p>
                        }
                    </div>
                </div>

                if unit.can_move == 1 {
                    <h2>{"Movement"}</h2>
                    <p>{"Max velocity: "}{format_f64(unit.max_velocity)}</p>
                    <p>{"Acceleration: "}{format_f64(unit.acceleration)}</p>
                    <p>{"Turn rate: "}{format_i64(unit.turn_rate)}</p>
                    <p>{"Brake rate: "}{format_f64(unit.brake_rate)}</p>
                }

                if unit.weapon_1.clone().or(unit.weapon_2.clone()).or(unit.weapon_3.clone()).is_some() {
                    <h2>{"Weapons"}</h2>
                    <div class="weapons">
                    if let Some(weapon_name) = unit.weapon_1.as_ref() {
                        <WeaponOverview weapon={weapons.get(weapon_name).unwrap().clone()} />
                    }
                    if let Some(weapon_name) = unit.weapon_2.as_ref() {
                        <WeaponOverview weapon={weapons.get(weapon_name).unwrap().clone()} />
                    }
                    if let Some(weapon_name) = unit.weapon_3.as_ref() {
                        <WeaponOverview weapon={weapons.get(weapon_name).unwrap().clone()} />
                    }
                    </div>
                }

                if unit.built_by.len() > 0 {
                    <h2>{"Built by"}</h2>
                    <div class="unit-class">
                    {
                        unit.built_by.iter().map(|unit_name| {
                            let builder = units.get(unit_name).unwrap().clone();
                            html! {
                                <UnitOverview key={unit_name.as_str()} unit={builder}/>
                            }
                        }).collect::<Html>()
                    }
                    </div>
                }

                if unit.builds.len() > 0 {
                    <h2>{"Builds"}</h2>
                    <div class="unit-class">
                    {
                        unit.builds.iter().map(|unit_name| {
                            if let Some(builder) = units.get(unit_name) {
                                html! {
                                    <UnitOverview key={unit_name.as_str()} unit={builder.clone()}/>
                                }
                            } else {
                                html! { <></> }
                            }
                        }).collect::<Html>()
                    }
                    </div>
                }
            </>
        }
    } else if units.len() == 0 {
        html! {
            <></>
        }
    } else {
        set_title("TA:Esc Units");
        html! {
            <h1>{ "This unit does not exist!" }</h1>
        }
    }
}

#[derive(Properties, PartialEq)]
pub struct UnitOverviewProps {
    pub unit: Unit,
}

#[function_component(UnitOverview)]
pub fn unit(props: &UnitOverviewProps) -> Html {
    let name = props.unit.name.clone();
    let img_url = format!("/data/unit_icons/{}.webp", props.unit.object_name.clone());
    html! {
        <div class="unit">
            <Link<Route> to={Route::Unit{unit_name: props.unit.unit_name.clone()}}>
                <span>{name}</span>
                <img src={img_url}/>
            </Link<Route>>
        </div>
    }
}

#[derive(Properties, PartialEq)]
pub struct WeaponOverviewProps {
    pub weapon: Weapon,
}

#[function_component(WeaponOverview)]
pub fn weapon(props: &WeaponOverviewProps) -> Html {
    let name = props.weapon.name.clone();
    html! {
        <div class="weapon">
            <h3>{name}</h3>
            <p>{ format!("Range: {}", props.weapon.range) }</p>
            <p>{ format!("Reload time: {}", props.weapon.reload_time) }</p>
            <p>{ format!("Energy per shot: {}", props.weapon.energy_per_shot) }</p>
            <p>{ format!("Weapon velocity: {}", props.weapon.weapon_velocity) }</p>
            <p>{ format!("Area of effect: {}", props.weapon.area_of_effect) }</p>
            <p>{ format!("Tolerance: {}", props.weapon.tolerance) }</p>
            <p>{ format!("Damage: {}", props.weapon.damage.get("default").unwrap_or(&0)) }</p>
        </div>
    }
}

use crate::app::{set_title, Route};
use crate::types::{EscDataCtx, Unit};
use js_sys::wasm_bindgen::closure::Closure;
use js_sys::wasm_bindgen::JsCast;
use web_sys::HtmlSelectElement;
use yew::prelude::*;
use yew::Properties;
use yew_router::prelude::*;

const CLASSES: [&'static str; 9] = [
    "COMMANDER",
    "KBOT",
    "VEHICLE",
    "AIRCRAFT",
    "SHIP",
    "HOVERCRAFT",
    "LAB",
    "RESOURCE",
    "BUILDING",
];

#[function_component(Units)]
pub fn units() -> Html {
    let esc_data = use_context::<EscDataCtx>().expect("no ctx found");
    let units = esc_data.units;

    set_title("TA:ESC Units | Index");

    let side_ref = use_node_ref();
    let side = use_state(|| "BOTH".to_string());
    {
        let side_ref = side_ref.clone();
        let side = side.clone();

        use_effect_with(side_ref, move |side_ref| {
            let select = side_ref
                .cast::<HtmlSelectElement>()
                .expect("side_ref not attached to select element");

            let listener = Closure::<dyn Fn(Event)>::wrap(Box::new(move |e: Event| {
                let select = e
                    .current_target()
                    .unwrap()
                    .dyn_into::<HtmlSelectElement>()
                    .unwrap();

                side.set(select.value());
            }));

            select
                .add_event_listener_with_callback("change", listener.as_ref().unchecked_ref())
                .unwrap();

            listener.forget();
        });
    }

    html! {
        <>
            <h1>{ "Units" }</h1>
            <div class="units-container">
            <div class="units-sidebar-container">
                <div class="units-sidebar-scroll-container">
                    <div class="units-sidebar">
                        <select ref={side_ref} name="side" id="side-selector">
                            <option value="BOTH" selected={*side == "BOTH"}>{"Both"}</option>
                            <option value="ARM" selected={*side == "ARM"}>{"Arm"}</option>
                            <option value="CORE" selected={*side == "CORE"}>{"Core"}</option>
                        </select>
                        <hr/>
                        {
                            (0..5).map(|i| {
                                html! {
                                    <>
                                        <a href={format!("#tier-{}", i)}>{ format!("Tier {}", i) }</a>
                                        <div>
                                            {
                                                CLASSES.into_iter()
                                                    .filter(|class| {
                                                        units.values()
                                                            .filter(|u| *side == "BOTH" || u.side == *side || u.side == "ALL")
                                                            .filter(|u| u.tier == i)
                                                            .filter(|u| u.rovi_class == *class)
                                                            .next()
                                                            .is_some()
                                                    })
                                                    .map(|class| {
                                                    html! {
                                                        <a href={format!("#tier-{}-{}", i, class)}>{ format!("{}", class) }</a>
                                                    }
                                                }).collect::<Html>()
                                            }
                                        </div>
                                    </>
                                }
                            }).collect::<Html>()
                        }
                    </div>
                </div>
            </div>
                <div class="units-list">
                    {
                        (0..5).map(|i| {
                            let tier_units: Vec<Unit> = units
                                .values()
                                .filter(|u| *side == "BOTH" || u.side == *side  || u.side == "ALL")
                                .filter(|u| u.tier == i)
                                .map(|u| u.clone())
                                .collect();

                            html! {
                                if tier_units.len() > 0 {
                                    <Tier key={i} tier={i} units={tier_units}/>
                                }
                            }
                        }).collect::<Html>()
                    }
                </div>
            </div>
        </>
    }
}

#[derive(Properties, PartialEq)]
pub struct TierProps {
    pub tier: i64,
    pub units: Vec<Unit>,
}

#[function_component(Tier)]
pub fn tier(props: &TierProps) -> Html {
    html! {
        <div class="unit-tier-container">
            <h2 id={format!("tier-{}", props.tier)}>{ format!("Tier {}", props.tier) }</h2>
            {
                CLASSES.into_iter().map(|class| {
                    let mut units: Vec<Unit> = props.units.clone()
                        .into_iter()
                        .filter(|u| u.rovi_class == class)
                        .collect();
                    units.sort_by_key(|u| !u.name.to_lowercase().contains("construction"));

                    if units.len() > 0 {
                        html! {
                            <Class key={class.to_string()} tier={props.tier} class_name={class.to_string()} units={units}/>
                        }
                    } else {
                        html! { <></> }
                    }
                }).collect::<Html>()
            }
        </div>
    }
}

#[derive(Properties, PartialEq)]
pub struct ClassProps {
    pub tier: i64,
    pub class_name: String,
    pub units: Vec<Unit>,
}

#[function_component(Class)]
pub fn class(props: &ClassProps) -> Html {
    html! {
        <div class="unit-class-container">
            <h3 id={format!("tier-{}-{}", props.tier, props.class_name.clone())}>{props.class_name.clone()}</h3>
            <div class="unit-class">
                {
                    props.units.clone().into_iter().map(|unit| {
                        let key = unit.object_name.clone();

                        html! {
                            <UnitOverview key={key} unit={unit.clone()}/>
                        }
                    }).collect::<Html>()
                }
            </div>
        </div>
    }
}

#[derive(Properties, PartialEq)]
pub struct UnitOverviewProps {
    pub unit: Unit,
}

#[function_component(UnitOverview)]
pub fn unit(props: &UnitOverviewProps) -> Html {
    let name = props.unit.name.clone();
    let img_url = format!("/data/unit_icons/{}.webp", props.unit.unit_name.clone());
    html! {
        <Link<Route> to={Route::Unit{unit_name: props.unit.unit_name.clone()}}>
            <div class="unit">
                <span>{name}</span>
                <img src={img_url}/>
            </div>
        </Link<Route>>
    }
}

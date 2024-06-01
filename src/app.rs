use std::collections::HashMap;

use gloo_net::http::Request;
use yew::prelude::*;
use yew_router::prelude::*;

use crate::types::{EscDataCtx, Unit, Weapon};
use crate::unit::UnitPage;
use crate::units::Units;

#[derive(Clone, Routable, PartialEq)]
pub enum Route {
    #[at("/")]
    Home,
    #[at("/units")]
    Units,
    #[at("/unit/:unit_name")]
    Unit { unit_name: String },
    #[at("/mirrors")]
    Mirrors,
    #[not_found]
    #[at("/404")]
    NotFound,
}

pub fn set_title(title: &str) {
    web_sys::window()
        .and_then(|w| w.document())
        .inspect(|d| d.set_title(title));
}

#[function_component(NavBar)]
pub fn nav_bar() -> Html {
    html! {
        <nav>
            <Link<Route> to={Route::Home}>{ "Home" }</Link<Route>>
            <Link<Route> to={Route::Units}>{ "Units" }</Link<Route>>
            <Link<Route> to={Route::Mirrors}>{ "Mirrors" }</Link<Route>>
            <a href="https://github.com/14ROVI/taesc-units" style="margin-left: auto;">{ "This website's GitHub" }</a>
        </nav>
    }
}

#[function_component(Home)]
pub fn home() -> Html {
    set_title("TA:ESC Units | Home");

    html! {
        <>
            <h1>{ "Home" }</h1>
            <p>
                { "Welcome to my website! Here you can find a complete list of the units in Escalation, " }
                { "up to date automatically. Also, I serve mirrors to download Escalation incase the TAU " }
                { "website is down and not working :)" }
            </p>
            <p>
                { "In the future I would like to expand this more but I'm not sure what into yet lol." }
            </p>
        </>
    }
}

#[function_component(Mirrors)]
pub fn mirrors() -> Html {
    set_title("TA:ESC Units | Mirrors");

    html! {
        <>
            <h1>{ "Mirrors" }</h1>
            <h2>{ "9.9.7" }</h2>
            <li><a href="/data/mirrors/ESC_997_FULL.zip">{ "ESC_997_FULL.zip" }</a>{ " " }<span>{ "(321MB)" }</span></li>
            <li><a href="/data/mirrors/ESC_997_FULL.rar">{ "ESC_997_FULL.rar" }</a>{ " " }<span>{ "(310MB)" }</span></li>
            <br/>
            <li><a href="/data/mirrors/ESC_997_FAST.zip">{ "ESC_997_FAST.zip" }</a>{ " " }<span>{ "(53MB)" }</span></li>
            <li><a href="/data/mirrors/ESC_997_FAST.rar">{ "ESC_997_FAST.rar" }</a>{ " " }<span>{ "(43MB)" }</span></li>
        </>
    }
}

fn switch(routes: Route) -> Html {
    web_sys::window().inspect(|w| w.scroll_to_with_x_and_y(0.0, 0.0));

    match routes {
        Route::Home => html! { <Home/> },
        Route::Units => html! { <Units/> },
        Route::Unit { unit_name } => html! { <UnitPage unit_name={unit_name}/> },
        Route::Mirrors => html! { <Mirrors/> },
        Route::NotFound => html! { <h1>{ "404" }</h1> },
    }
}

#[function_component(App)]
pub fn app() -> Html {
    let ctx = use_state(|| EscDataCtx {
        units: HashMap::new(),
        weapons: HashMap::new(),
    });

    {
        let ctx = ctx.clone();

        use_effect_with((), move |_| {
            let ctx = ctx.clone();
            wasm_bindgen_futures::spawn_local(async move {
                let units: HashMap<String, Unit> = Request::get("/data/units.json")
                    .send()
                    .await
                    .unwrap()
                    .json()
                    .await
                    .unwrap();

                let weapons: HashMap<String, Weapon> = Request::get("/data/weapons.json")
                    .send()
                    .await
                    .unwrap()
                    .json()
                    .await
                    .unwrap();

                ctx.set(EscDataCtx { units, weapons });
            });

            || ()
        });
    }

    html! {
        <ContextProvider<EscDataCtx> context={(*ctx).clone()}>
            <BrowserRouter>
                <NavBar/>
                <main>
                    <Switch<Route> render={switch} />
                </main>
            </BrowserRouter>
        </ContextProvider<EscDataCtx>>
    }
}

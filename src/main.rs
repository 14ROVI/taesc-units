mod app;
mod types;
mod unit;
mod units;
use app::App;
use wasm_logger;

fn main() {
    wasm_logger::init(wasm_logger::Config::default());
    yew::Renderer::<App>::new().render();
}

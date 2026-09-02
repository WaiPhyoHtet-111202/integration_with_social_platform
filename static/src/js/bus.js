// import { registry } from "@web/core/registry";
//
// export const TeleMessage = {
//     dependencies: ["bus_service", "notification"],
//     start(env, { bus_service, notification,action }) {
//         bus_service.addChannel("telegram_updates");
//
//         bus_service.subscribe("telegram_message", (payload) => {
//             console.log("Telegram Update Received:", payload);
//
//
//             notification.add(payload.message, {
//                 title: payload.type,
//                 type: "info",
//             });
//             const currentView = action.currentController;
//             console.log(currentView);
//         });
//     }
// };
//
// registry.category("services").add("tele_message", TeleMessage);
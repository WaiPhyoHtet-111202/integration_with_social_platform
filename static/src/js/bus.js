// import {useService} from "@web/core/utils/hooks";
// import {Component,onMounted,onWillUnmount,App,xml} from "@odoo/owl"
// import {registry} from "@web/core/registry";
//
//
// export class BusService extends Component {
//     setup() {
//         console.log("Hello World");
//         // this.bus = useService('bus_service');
//         this.busService = useService("bus_service");
//         console.log(`Bus Service : ${this.busService}`);
//         this.notification = useService('notification');
//         this.channel = 'telegram_updates';
//
//         // When Component Start To Add Channel and To Add this to onNotification Function and To start Bus Service
//         onMounted(() => {
//             this.busService.addChannel(this.channel);
//             this.busService.addEventListener('notification',this.onNotification.bind(this));
//             this.busService.start();
//         });
//
//         // To Delete Bus Channel After Deleting Component
//         onWillUnmount(() => {
//             this.busService.deleteChannel(this.channel);
//         });
//
//     };
//
//     onNotification(event)  {
//         console.log('Js file is start running');
// };
// }
//
// registry.category('services').add('telegram_bus_service',BusService)

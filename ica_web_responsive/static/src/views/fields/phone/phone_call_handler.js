import { isMobileOS } from "@web/core/browser/feature_detection";
import { phoneCallHandlerRegistry } from "@web/core/phone/phone_call";
import { user } from "@web/core/user";
import { PhoneInstallDialog } from "@ica_web_responsive/views/fields/phone/phone_install_dialog";

phoneCallHandlerRegistry.add("phone_install_dialog", {
    isApplicable(env) {
        return !isMobileOS() && user.isSystem && !env.services.voip;
    },

    execute(env) {
        env.services.dialog.add(PhoneInstallDialog);
        return false;
    },
});

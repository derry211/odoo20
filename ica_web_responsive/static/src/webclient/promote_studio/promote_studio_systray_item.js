import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { user } from "@web/core/user";
import { PromoteStudioDialog } from "@ica_web_responsive/webclient/promote_studio/promote_studio_dialog";
import { _t } from "@web/core/l10n/translation";

import { Component } from "@odoo/owl";

export class PromoteStudioSystrayItem extends Component {
    static template = "ica_web_responsive.SystrayItem";

    setup() {
        this.dialog = useService("dialog");
    }

    _onClick() {
        this.dialog.add(PromoteStudioDialog, {
            title: _t("Odoo Studio - Add new fields to any view"),
        });
    }
}

export const promoteStudioSystrayItem = {
    Component: PromoteStudioSystrayItem,
    isDisplayed: () => user.isSystem,
};

registry
    .category("systray")
    .add("PromoteStudioSystrayItem", promoteStudioSystrayItem, { sequence: 1 });

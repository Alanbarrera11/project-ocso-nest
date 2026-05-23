    import { applyDecorators, UseGuards } from "@nestjs/common";
    import { AuthGuard } from "../guards/auth.guards";
    import { RolesGuard } from "../guards/roles.guards";
    import { Roles } from "./roles.decorator";
import { ROLES } from "../constants/roles.constants";

    //aqui se evaluan decoradores al mismo tiempo para en el controlador usarlo solo como @auth
    export const Auth = (...roles : ROLES[]) => {
        roles.push(ROLES.ADMIN);
    return applyDecorators(
        Roles(roles),
        UseGuards(AuthGuard, RolesGuard)
    )
        
    }
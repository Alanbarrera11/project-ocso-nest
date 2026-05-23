import { createParamDecorator, ExecutionContext } from "@nestjs/common";

//esto es un decorador personalizado 

export const UserData  /* nombre del decorador*/= createParamDecorator(
    (data: unknown, ctx: ExecutionContext) => {
        const request = ctx.switchToHttp().getRequest(); //de aqui se obtiene la request 
        return request.user; //aqui se retorna lo que le agrego el authguard (la parte de requiest user)
    },

)
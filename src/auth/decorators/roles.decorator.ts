    import { Reflector } from "@nestjs/core"
    import { notStrictEqual } from "assert"

    export const Roles = Reflector.createDecorator<string[]>();
    //evalua roles que van pasando al decorador en un arreglo de strings    
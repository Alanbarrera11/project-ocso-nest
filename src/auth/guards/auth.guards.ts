// El AuthGuard es un guardián que intercepta cada request antes de que llegue al controlador y verifica:  PROTEGE LAS RUTAS PARA QUE NO CUALQUIERA TENGA ACCESO

// Que el token existe — si no hay token, rechaza
// Que la firma es válida — verifica con la clave secreta
// Que no ha expirado — revisa el expiresIn
// Que el usuario existe — opcional, pero se puede agregar  
// Request → AuthGuard verifica token → ✅ pasa al controlador
//                                    → ❌ lanza 401 Unauthorized

import {
    CanActivate,
    ExecutionContext,
    Injectable,
    UnauthorizedException,
} from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { JWT_KEY } from '../constants/jwt.constants';
import { Request } from 'express';

@Injectable()
export class AuthGuard implements CanActivate {
    constructor(private jwtService: JwtService) {}
private extractTokenFromHeader(request: Request): string | undefined {
    const [type, token] = request.headers.authorization?.split(' ') ?? [];
    return type === 'Bearer' ? token : undefined;
}
    async canActivate(context: ExecutionContext): Promise<boolean> {
        const request = context.switchToHttp().getRequest();
        const token = this.extractTokenFromHeader(request);
        if (!token) {
            throw new UnauthorizedException();
        }
        try {
            const payload = await this.jwtService.verifyAsync(
                token,
                {
                    secret: JWT_KEY
                }
            );
            request['user'] = payload;  //aqui se almacena toda la informacion que se haya recolectado del payload, es la info que se la graba a cada 
            //token. En este caso son las propiedades del user
        } catch {
            throw new UnauthorizedException();
        }
        return true;
    }
}
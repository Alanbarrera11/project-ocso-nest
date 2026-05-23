// ❌ 1. Falta coma después de TypeOrmModule.forFeature([User])
// ❌ 2. jwtModule en minúscula
// ❌ 3. JWT_KEY y EXPIRES_IN no están definidos

import { Module } from '@nestjs/common';
import { AuthService } from './auth.service';
import { AuthController } from './auth.controller';
import { TypeOrmModule } from '@nestjs/typeorm';
import { User } from './entities/user.entity';
import { JwtModule } from '@nestjs/jwt';
import { EXPIRES_IN, JWT_KEY } from './constants/jwt.constants';

@Module({
  imports: [
    TypeOrmModule.forFeature([User]),  // ← coma aquí
    JwtModule.register({               // ← mayúscula
        secret: JWT_KEY,  // ← desde .env
        signOptions: { 
            expiresIn: EXPIRES_IN ,
        },
        global: true
    })
  ],
  controllers: [AuthController],
  providers: [AuthService],
})
export class AuthModule {}
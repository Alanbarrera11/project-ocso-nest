import { Module } from '@nestjs/common';
import { ProvidersService } from './providers.service';
import { ProvidersController } from './providers.controller';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Provider } from './entities/provider.entity';
import { JwtModule } from '@nestjs/jwt';
import { JWT_KEY } from 'src/auth/constants/jwt.constants';
import { EXPIRES_IN } from 'src/auth/constants/jwt.constants';
import { AuthGuard } from 'src/auth/guards/auth.guards';

@Module({
  
  imports:[TypeOrmModule.forFeature([Provider]),
JwtModule.register({
          secret: JWT_KEY,  // ← desde .env
                signOptions: { 
                    expiresIn: EXPIRES_IN ,
   }} ),],
  
  controllers: [ProvidersController],
  providers: [ProvidersService],
})
export class ProvidersModule {}

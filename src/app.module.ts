import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { EmployeesModule } from './employees/employees.module';
import { ProductsModule } from './products/products.module';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ConfigModule } from '@nestjs/config';
import { ProvidersModule } from './providers/providers.module';
import { Product } from './products/entities/product.entity';
import { Employee } from './employees/entities/employee.entity';
import { Provider } from './providers/entities/provider.entity';
import { ManagersModule } from './managers/managers.module';
import { LocationsModule } from './locations/locations.module';
import { RegionsModule } from './regions/regions.module';
import { AuthModule } from './auth/auth.module';
import { JwtModule } from '@nestjs/jwt';
import { JWT_KEY } from './auth/constants/jwt.constants';
import { EXPIRES_IN } from './auth/constants/jwt.constants';
@Module({
  imports: [
    ConfigModule.forRoot(),
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: process.env.host,
      port: +(process.env.port || '5432'),      
      username: 'postgres',
      password: process.env.pass,
      database: process.env.name,
      entities: [Product, Employee, Provider],
      autoLoadEntities:true,
      synchronize: true,
  }),
  EmployeesModule, ProductsModule, ProvidersModule, ManagersModule, LocationsModule, RegionsModule, AuthModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}

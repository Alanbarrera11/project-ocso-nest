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
  EmployeesModule, ProductsModule, ProvidersModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}

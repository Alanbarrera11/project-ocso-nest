import { Controller, Get, Post, Body, Patch, Param, Delete, NotFoundException, UseGuards, UnauthorizedException } from '@nestjs/common';
import { ProvidersService } from './providers.service';
import { CreateProviderDto } from './dto/create-provider.dto';
import { UpdateProviderDto } from './dto/update-provider.dto';
import { NotFoundError } from 'rxjs';
import { UserData } from 'src/auth/decorators/user.decorator';
import { User } from 'src/auth/entities/user.entity';
import { Roles } from 'src/auth/decorators/roles.decorator';
import { Auth } from 'src/auth/decorators/auth.decorator';
import { ROLES } from 'src/auth/constants/roles.constants';
import { ApiAuth } from 'src/auth/decorators/api.decorator';


@ApiAuth()
@Controller('providers')
export class ProvidersController {
  constructor(private readonly providersService: ProvidersService) {}
  @Auth( ROLES.MANAGER)
  @Post()
  create(@Body() createProviderDto: CreateProviderDto) {
    return this.providersService.create(createProviderDto);
  }
  @Auth(ROLES.EMPLOYEE, ROLES.MANAGER)
  @Get()
  findAll(@UserData() user : User) {  //aqui se usa el decorador de user 
    if(user.userRoles.includes("Employee")) throw new UnauthorizedException("No estas autorizado, solo admins y managers ") //esta es la manera mas facil de limitar el acceso del usuario sin necesidad de hacer un quiery para ver sy rol
    return this.providersService.findAll();
  }
  @Auth(ROLES.EMPLOYEE, ROLES.MANAGER)
  @Get('/name/:name')
  async findByName(@Param('name') name :string){
    return this.providersService.findOneByName(name);
  }

  @Auth(ROLES.EMPLOYEE, ROLES.MANAGER)
  @Get(':id')
  findOne(@Param('id') id: string) {
    const provider = this.providersService.findOne(id);
    if(!provider) throw new NotFoundException()
      return provider
  }
  @Auth( ROLES.MANAGER)
  @Patch(':id')
  update(@Param('id') id: string, @Body() updateProviderDto: UpdateProviderDto) {
    return this.providersService.update(id, updateProviderDto);
  }
  @Auth( ROLES.MANAGER)
  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.providersService.remove(id);
  }
}

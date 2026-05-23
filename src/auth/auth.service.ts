import { Injectable, NotFoundException, UnauthorizedException } from '@nestjs/common';
import { CreateUserDto } from './dto/create-user.dto';
import { UpdateUserDto } from './dto/update-user.dto';
import { InjectEntityManager, InjectRepository } from '@nestjs/typeorm';
import { User } from './entities/user.entity';
import { Repository } from 'typeorm';
import * as bcrypt from "bcrypt"
import { JwtService } from '@nestjs/jwt';
import { privateDecrypt } from 'crypto';
import { LoginUserDto } from './dto/login-user-dto';
import { NotFoundError } from 'rxjs';
@Injectable()
export class AuthService {
constructor(
  @InjectRepository(User) private userRepository: Repository<User>,
  private jwtService:  JwtService,   // de aqui se importa el jwt. Se declara la variable jwtService de tipo JwtServie
){}
registerUser(createUserDto: CreateUserDto){
  createUserDto.userPassword = bcrypt.hashSync(createUserDto.userPassword, 5)
  return this.userRepository.save(createUserDto)
}

async loginUser(loginUserDto: LoginUserDto){
  const user = await this.userRepository.findOne({
    where:{
      userEmail: loginUserDto.userEmail
    }
  })
  if (!user) throw new UnauthorizedException("credenciales incorrectas")
  const match = await bcrypt.compare(loginUserDto.userPassword, user.userPassword)
  if(!match) throw new UnauthorizedException("No estas autorizado");


  //aqui se hace el uso de jwt donde se lleva a cabo lo de los tokens 
 const payload = {
  userEmail : user.userEmail,
  userPassword: user.userPassword,
  userRoles: user.userRoles
 };
 const token = this.jwtService.sign(payload);
 return token;
}

async updateUser(userEmail:string, updateUserDto:UpdateUserDto){
  const newUserData = await this.userRepository.preload({
userEmail,
...updateUserDto
  })
      if (!newUserData) throw new NotFoundException()
  
  this.userRepository.save(newUserData)
  return newUserData
}
}

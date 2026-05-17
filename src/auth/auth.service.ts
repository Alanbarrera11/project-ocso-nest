import { Injectable, UnauthorizedException } from '@nestjs/common';
import { CreateUserDto } from './dto/create-user.dto';
import { UpdateUserDto } from './dto/update-user.dto';
import { InjectEntityManager, InjectRepository } from '@nestjs/typeorm';
import { User } from './entities/user.entity';
import { Repository } from 'typeorm';
import * as bcrypt from "bcrypt"
import * as jwt from 'jsonwebtoken'
@Injectable()
export class AuthService {
constructor(
  @InjectRepository(User) private userRepository: Repository<User>
){}
registerUser(createUserDto: CreateUserDto){
  createUserDto.userPassword = bcrypt.hashSync(createUserDto.userPassword, 5)
  return this.userRepository.save(createUserDto)
}

async loginUser(createUserDto: CreateUserDto){
  const user = await this.userRepository.findOne({
    where:{
      userEmail: createUserDto.userEmail
    }
  })
  if (!user) throw new UnauthorizedException("credenciales incorrectas")
  const match = await bcrypt.compare(createUserDto.userPassword, user.userPassword)
  if(!match) throw new UnauthorizedException("No estas autorizado");
  const token = jwt.sign(JSON.stringify(user), "SECRET USER")
  return ;
}


}

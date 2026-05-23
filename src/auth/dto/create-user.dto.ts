import { IsEmail, IsIn, IsOptional, IsString, MinLength } from "class-validator";
import { User } from "../entities/user.entity";

export class CreateUserDto extends User {

    @IsEmail()
   declare userEmail: string;
   @IsString()
   @MinLength(8)
   declare userPassword: string;
   @IsOptional()
   @IsIn(["Admin", "Employee", "Manager"])
   declare userRoles: string[];
}

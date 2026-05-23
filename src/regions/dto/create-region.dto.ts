import { IsArray, IsObject, IsOptional, IsString, MaxLength } from "class-validator";
import { Region } from "../entities/region.entity";

export class CreateRegionDto extends Region {
    @IsString()
    @MaxLength(100)
    declare regionName: string;
    @IsArray()
    declare regionStates: string[];
    @IsObject()
    @IsOptional()
    declare region:Region;
}
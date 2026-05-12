import {IsInt, IsNumber, IsOptional, IsString, IsUUID, MaxLength } from "class-validator";
import { Product } from "../entities/product.entity";
import { Provider } from "../../providers/entities/provider.entity";

export class CreateProductDto extends Product  {
    @IsString()
    @IsUUID("4")
    @IsOptional()
    declare productId: string;
    @IsString()
    @MaxLength(40)
    declare productName: string;
    @IsNumber()
    declare price: number;
    @IsInt()
    declare countSeal: number;
    @IsString()
    @IsUUID("4")
    declare provider: Provider;
}

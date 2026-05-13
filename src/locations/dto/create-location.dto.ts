import { ArrayNotEmpty, IsArray, IsString, MaxLength } from "class-validator";

export class CreateLocationDto extends Location {
    @IsString()
    @MaxLength(35)
    locationName: string;
    @IsString()
    @MaxLength(160)
    locationAdress;
    @IsArray()
    @ArrayNotEmpty()
    locationLatLng: number[];
}

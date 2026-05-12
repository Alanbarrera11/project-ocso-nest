import { Provider } from "src/providers/entities/provider.entity";
import { Column, Entity, ManyToOne, PrimaryColumn, PrimaryGeneratedColumn } from "typeorm";
   @Entity()
export class Product {
    @PrimaryGeneratedColumn("uuid")
    productId: string;
    @Column({type: "text"})
    productName: string;
    @Column({type: "float"})
    price: number;
    @Column({type: "int"})
    countSeal: number;
   // @Column({type: "uuid"})
    //provider: string;
    @ManyToOne(() => Provider, (provider) => provider.product)
    provider:Provider
}
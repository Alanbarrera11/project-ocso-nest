import { Injectable, NotFoundException } from '@nestjs/common';
import { CreateProductDto } from './dto/create-product.dto';
import { UpdateProductDto } from './dto/update-product.dto';
import { v4 as uuid } from 'uuid';
import { Product } from './entities/product.entity';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { not } from 'supertest/lib/cookies';

@Injectable()
export class ProductsService {
  constructor(
    @InjectRepository(Product)
    private productRepository: Repository<Product>
  ){}

  create(createProductDto: CreateProductDto) {
   const product = this.productRepository.save(createProductDto)
   return product
  }

  findAll() {
    return this.productRepository.find();
  }

  findOne(id: string) {
  const product = this.productRepository.findOneBy({
    productId: id,
  })
  if (!product) throw new NotFoundException()
    return product;

  }
  // findByProvider(id: string) {
  //   const productFound = this.products.filter((product) => product.provider === id)
  //   if(productFound.length ===0) throw new NotFoundException()
  //     return productFound;
  // }

 async update(id: string, UpdateProductDto: UpdateProductDto) {
   const productToUpdate = await this.productRepository.preload({
    productId: id,
    ...UpdateProductDto
   })
   if (!productToUpdate) throw new NotFoundException() 
    this.productRepository.save(productToUpdate);
  return productToUpdate;
    }
  
      
  

  remove(id: string) {
   this.findOne(id)
  this.productRepository.delete({
    productId: id,
  })
  return{
    message: `objeto con id ${id} eliminado`
  }
  }

}
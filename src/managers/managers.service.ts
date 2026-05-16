import { BadRequestException, Injectable } from '@nestjs/common';
import { CreateManagerDto } from './dto/create-manager.dto';
import { UpdateManagerDto } from './dto/update-manager.dto';
import { Manager } from './entities/manager.entity';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
@Injectable()
export class ManagersService {
  constructor(
  @InjectRepository(Manager)
      private managerRepository:Repository<Manager>
    ){}

  create(createRegionDto: CreateManagerDto) {
      return this.managerRepository.save(createRegionDto);
    }
  
    findAll() {
  
      return this.managerRepository.find();
    }
  
    findOne(id: string) {
      const region = this.managerRepository.findOneBy({
        managerId:id,
      });
    }
  
   async update(id: string, updateLocationDto: UpdateManagerDto) {
       const managerToUpdate = await this.managerRepository.preload({
         managerId: id,
         ...UpdateManagerDto,
       })
       if (!managerToUpdate) throw new BadRequestException();
       return this.managerRepository.save(managerToUpdate)
      }
     remove(id: string) {
      return this.managerRepository.delete({
        managerId:id
      });
    }
  }
  
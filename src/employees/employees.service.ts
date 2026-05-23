import { Injectable, NotFoundException } from '@nestjs/common';
import { CreateEmployeeDto } from './dto/create-employee.dto';
import { UpdateEmployeeDto } from './dto/update-employee.dto';
import { v4 as uuid } from 'uuid';
import {InjectRepository} from '@nestjs/typeorm';
import {NumericType, Repository} from 'typeorm';
import {Employee} from './entities/employee.entity';


@Injectable()
export class EmployeesService {
 constructor(
  @InjectRepository(Employee)
  private employeeRepository: Repository<Employee>
 ){}

 findByLocation(id: number){
  return this.employeeRepository.findBy({
    location:{
      locationId: id
    }
  })
 }

  async create(createEmployeeDto: CreateEmployeeDto) {
    const employee =this.employeeRepository.create(createEmployeeDto)
    return await this.employeeRepository.save(employee)
  }

  findAll() {
   return this.employeeRepository.find();
  }

  findOne(id: string) {
    const employee = this.employeeRepository.findOneBy({
      employeeId : id,
    
    }
    )
    return employee;
  }
async update(id: string, updateEmployeeDto: UpdateEmployeeDto) {
    const employeeToUpdate = await this.employeeRepository.preload({
        employeeId: id,
        ...updateEmployeeDto
    }) 
    if (!employeeToUpdate) throw new NotFoundException() // ← primero verifica que existe
    await this.employeeRepository.save(employeeToUpdate) // ← ahora TypeScript sabe que no es undefined
    return employeeToUpdate
}
  remove(id: string) {
    this.employeeRepository.delete({
        employeeId: id
    }
    )
    return{
      message: "employee deleted"
    }
  }
}

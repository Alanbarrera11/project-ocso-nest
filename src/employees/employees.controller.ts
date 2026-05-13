import { Controller, Get, Post, Body, Patch, Param, Delete, ParseUUIDPipe, UseInterceptors, UploadedFile } from '@nestjs/common';
import { EmployeesService } from './employees.service';
import { CreateEmployeeDto } from './dto/create-employee.dto';
import { UpdateEmployeeDto } from './dto/update-employee.dto';
import { FileInterceptor } from '@nestjs/platform-express';

@Controller('employees')
export class EmployeesController {
  constructor(private readonly employeesService: EmployeesService) {}

  @Post()
  create(@Body() createEmployeeDto: CreateEmployeeDto) {
    return this.employeesService.create(createEmployeeDto);
  }

  @Get()
  findAll() {
    return this.employeesService.findAll();
  }

  @Post('upload')
  @UseInterceptors(FileInterceptor('file'))
  uploadPhoto(@UploadedFile() file : Express.Multer.File){
    console.log(file)
    return "ok";
  }

  @Get(':id') //se manda el id dentro de una urls
  findOne( //se busca ese id 
    @Param('id', new ParseUUIDPipe({version:'4'})) //con ese parametro
    id: string //se convierte en string y se almacena en esa variable
  ) {
    return this.employeesService.findOne(id); //se usa +1 para convertir ese string a number
  }

  @Patch(':id')
  update(@Param('id' ,new ParseUUIDPipe({version:'4'})) id: string, @Body() updateEmployeeDto: UpdateEmployeeDto) {
    return this.employeesService.update(id, updateEmployeeDto);
  }

  @Delete(':id')
  remove(@Param('id', new ParseUUIDPipe({version:'4'})) id: string) {
    return this.employeesService.remove(id);
  }
}

<?php

//use Illuminate\Database\Schema\Blueprint;
use Jenssegers\Mongodb\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateMongoCveDescsTable extends Migration
{
    /**
     * The name of the database connection to use.
     *
     * @var string
     */
    protected $connection = 'mongodb';

    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        //Schema::create('mongo_cve_descs', function (Blueprint $table) {
        Schema::connection($this->connection)->create('mongo_cve_descs', function (Blueprint $collection) {
            $collection->bigIncrements('id');
            $collection->timestamps();
            $collection->string('cve_id')->unique();
            $collection->text('desc');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::connection($this->connection)->drop('mongo_cve_descs');
    }
}

<?php

//use Illuminate\Database\Schema\Blueprint;
use Jenssegers\Mongodb\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateMongoTodayUsersTable extends Migration
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
        //Schema::create('mongo_today_users', function (Blueprint $table) {
        Schema::connection($this->connection)->create('mongo_today_users', function (Blueprint $collection) {
            $collection->bigIncrements('id');
            $collection->timestamps();
            $collection->date('date')->nullable();
            $collection->string('sid')->nullable();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        //Schema::drop('mongo_today_users');
        Schema::connection($this->connection)->drop('mongo_today_users');
    }
}

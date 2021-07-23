<?php

use Jenssegers\Mongodb\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateMongoWirelessTestsTable extends Migration
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
        Schema::connection($this->connection)->create('mongo_wireless_tests', function (Blueprint $collection) {
            $collection->bigIncrements('id');
            $collection->timestamps();
            $collection->string('type')->nullable(); // test type
            $collection->string('type_name')->nullable(); // test 이름
            $collection->string('session_id')->nullable(); //session id
            $collection->string('file_name')->nullable(); // rand 파일명
            $collection->string('file_md5')->nullable(); // md5
            $collection->string('start_time_at')->nullable(); // start 클릭
            //
            $collection->json('result')->nullable(); // 결과 json
            //
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::connection($this->connection)->drop('mongo_wireless_tests');
    }
}

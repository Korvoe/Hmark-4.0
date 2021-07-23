<?php

//use Illuminate\Database\Schema\Blueprint;
use Jenssegers\Mongodb\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateMongoTlsTestsTable extends Migration
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
        //Schema::create('mongo_tls_tests', function (Blueprint $table) {
        Schema::connection($this->connection)->create('mongo_tls_tests', function (Blueprint $collection) {
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
        //Schema::drop('mongo_tls_tests');
        Schema::connection($this->connection)->drop('mongo_tls_tests');
    }
}

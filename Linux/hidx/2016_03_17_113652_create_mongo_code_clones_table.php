<?php

//use Illuminate\Database\Schema\Blueprint;
use Jenssegers\Mongodb\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateMongoCodeClonesTable extends Migration
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
        //Schema::create('mongo_code_clones', function (Blueprint $collection) {
        Schema::connection($this->connection)->create('mongo_code_clones', function (Blueprint $collection) {
            $collection->bigIncrements('id');
            $collection->timestamps();
            $collection->string('type')->nullable(); // test type
            $collection->string('type_name')->nullable(); // test 이름
            $collection->string('session_id')->nullable(); //session id
            $collection->string('file_name')->nullable(); // rand 파일명
            $collection->string('file_md5')->nullable(); // md5
            $collection->string('start_time_at')->nullable(); // start 클릭
            $collection->string('queue_status')->nullable(); // job (queue) 상태
            $collection->string('job_handle_time_at')->nullable(); // job handle 시각
            $collection->string('job_run_start_time_at')->nullable(); // job - python script 시작
            $collection->string('job_run_end_time_at')->nullable(); // job - python script 종료
            $collection->string('job_run_diff_time')->nullable(); // job - diff time
            $collection->string('rate')->default('0'); // 진행률
            $collection->string('result_status')->nullable(); // 결과 상태
            $collection->boolean('p_isSuccessful')->default(false); // python script 성공
            // 이하 > py 에서 리턴
            $collection->string('p_start_time_at')->nullable(); // python script 시작
            $collection->string('p_end_time_at')->nullable(); // python script 종료
            $collection->string('p_elapsed_time')->nullable(); // python script 내부 시간
            $collection->bigInteger('file_count')->nullable(); // file_count
            $collection->bigInteger('func_count')->nullable(); // func_count
            $collection->bigInteger('line_count')->nullable(); // line_count
            $collection->string('script_version')->nullable(); // script_version
            $collection->string('pool_version')->nullable(); // pool_version
            $collection->integer('total_number')->nullable(); // 전체 개수
            $collection->integer('total_cve_number')->nullable(); // 전체 cve 개수
            $collection->string('result_level')->nullable(); // 취약점 정도
            $collection->json('result')->nullable(); // 결과 json
            $collection->json('top_vulfile')->nullable(); // 가장 취약점이 많이 검출된 파일
            $collection->json('top_cve')->nullable(); // 가장 많이 검출된 CVE
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        //Schema::drop('mongo_code_clones');
        Schema::connection($this->connection)->drop('mongo_code_clones');
    }
}

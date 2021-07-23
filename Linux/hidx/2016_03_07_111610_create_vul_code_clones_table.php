<?php

use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateVulCodeClonesTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('vul_code_clones', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->timestamps();
            $table->string('type')->nullable(); // test type
            $table->string('type_name')->nullable(); // test 이름
            $table->string('session_id')->nullable(); //session id
            $table->string('file_name')->nullable(); // rand 파일명
            $table->string('file_md5')->nullable(); // md5
            $table->string('start_time_at')->nullable(); // start 클릭
            $table->string('queue_status')->nullable(); // job (queue) 상태
            $table->string('job_handle_time_at')->nullable(); // job handle 시각
            $table->string('job_run_start_time_at')->nullable(); // job - python script 시작
            $table->string('job_run_end_time_at')->nullable(); // job - python script 종료
            $table->string('job_run_diff_time')->nullable(); // job - diff time
            $table->string('rate')->default('0'); // 진행률
            $table->string('result_status')->nullable(); // 결과 상태
            $table->boolean('p_isSuccessful')->default(false); // python script 성공
            // 이하 > py 에서 리턴
            $table->string('p_start_time_at')->nullable(); // python script 시작
            $table->string('p_end_time_at')->nullable(); // python script 종료
            $table->string('p_elapsed_time')->nullable(); // python script 내부 시간
            $table->bigInteger('file_count')->nullable(); // file_count
            $table->bigInteger('func_count')->nullable(); // func_count
            $table->bigInteger('line_count')->nullable(); // line_count
            $table->string('script_version')->nullable(); // script_version
            $table->string('pool_version')->nullable(); // pool_version
            $table->integer('total_number')->nullable(); // 전체 개수
            $table->string('result_level')->nullable(); // 취약점 정도

            //20160330 mariadb 에서는 안된다?? >> text
            //$table->json('result')->nullable(); // 결과 json
            $table->text('result')->nullable(); // 결과 json
            $table->text('top_vulfile')->nullable(); // 가장 취약점이 많이 검출된 파일
            $table->text('top_cve')->nullable(); // 가장 많이 검출된 CVE
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::drop('vul_code_clones');
    }
}

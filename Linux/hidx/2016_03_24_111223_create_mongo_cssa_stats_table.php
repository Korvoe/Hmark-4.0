<?php

//use Illuminate\Database\Schema\Blueprint;
use Jenssegers\Mongodb\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateMongoCssaStatsTable extends Migration
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
        //Schema::create('mongo_cssa_stats', function (Blueprint $table) {
        Schema::connection($this->connection)->create('mongo_cssa_stats', function (Blueprint $collection) {
            $collection->bigIncrements('id');
            $collection->timestamps();
            $collection->integer('user_count')->default(0);
            $collection->bigInteger('bf1_count')->default(0);
            $collection->bigInteger('bf2_count')->default(0);
            $collection->bigInteger('wf1_count')->default(0);
            $collection->bigInteger('wf1_file_count')->default(0);
            $collection->bigInteger('wf1_func_count')->default(0);
            $collection->bigInteger('wf1_line_count')->default(0);
            $collection->bigInteger('nf1_count')->default(0);
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        //Schema::drop('mongo_cssa_stats');
        Schema::connection($this->connection)->drop('mongo_cssa_stats');
    }
}

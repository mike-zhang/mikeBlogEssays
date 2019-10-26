kaldi使用cvte模型进行语音识别
===================================================

操作系统 ： Unbutu18.04_x64

gcc版本 ：7.4.0


该模型在thch30数据集上测试的错误率只有8.25%，效果还是不错的。

模型下载地址：

http://www.kaldi-asr.org/models/m2

选择模型：CVTE Mandarin Model V2


测试文本： 

自然语言理解和生成是一个多方面问题，我们对它可能也只是部分理解。


在线识别
---------------------------------------------------------------------

测试脚本
::


    ./online2-wav-nnet3-latgen-faster --do-endpointing=false --online=false --feature-type=fbank --fbank-config=../../egs/cvte/s5/conf/fbank.conf --max-active=7000 --beam=15.0 --lattice-beam=6.0 --acoustic-scale=1.0 --word-symbol-table=../../egs/cvte/s5/exp/chain/tdnn/graph/words.txt ../../egs/cvte/s5/exp/chain/tdnn/final.mdl ../../egs/cvte/s5/exp/chain/tdnn/graph/HCLG.fst 'ark:echo utter1 utter1|' 'scp:echo utter1 /tmp/test1.wav|' ark:/dev/null

识别结果：
::

    LOG (online2-wav-nnet3-latgen-faster[5.5.421~1453-85d1a]:RemoveOrphanNodes():nnet-nnet.cc:948) Removed 1 orphan nodes.
    LOG (online2-wav-nnet3-latgen-faster[5.5.421~1453-85d1a]:RemoveOrphanComponents():nnet-nnet.cc:847) Removing 2 orphan components.
    LOG (online2-wav-nnet3-latgen-faster[5.5.421~1453-85d1a]:Collapse():nnet-utils.cc:1463) Added 1 components, removed 2
    LOG (online2-wav-nnet3-latgen-faster[5.5.421~1453-85d1a]:CompileLooped():nnet-compile-looped.cc:345) Spent 0.00508595 seconds in looped compilation.
    utter1 自然语言 理解 和 生成 时 你 该 付 多少 拗 暗 批 我们 对 他 能 爷 只是 部分 理解
    LOG (online2-wav-nnet3-latgen-faster[5.5.421~1453-85d1a]:main():online2-wav-nnet3-latgen-faster.cc:286) Decoded utterance utter1
    LOG (online2-wav-nnet3-latgen-faster[5.5.421~1453-85d1a]:Print():online-timing.cc:55) Timing stats: real-time factor for offline decoding was 0.442773 = 3.21453 seconds  / 7.26 seconds.
    LOG (online2-wav-nnet3-latgen-faster[5.5.421~1453-85d1a]:main():online2-wav-nnet3-latgen-faster.cc:292) Decoded 1 utterances, 0 with errors.
    LOG (online2-wav-nnet3-latgen-faster[5.5.421~1453-85d1a]:main():online2-wav-nnet3-latgen-faster.cc:294) Overall likelihood per frame was 1.84166 per frame over 724 frames.


可以看到，在线识别的效果比较差。


离线识别
---------------------------------------------------------------------

1、直接用cvte自带的脚本进行识别

替换声音文件后，执行如下操作：
::

    ln -s ~/kaldi/egs/wsj/s5/steps ~/kaldi/egs/cvte/s5/steps
    ln -s ~/kaldi/egs/wsj/s5/utils ~/kaldi/egs/cvte/s5/utils
    cd egs/cvte/s5
    ./run.sh


查看结果 ：
::

    mike@local:~/src/kaldi/egs/cvte/s5/exp$ cat chain/tdnn/decode_test/scoring_kaldi/penalty_1.0/10.txt
    CVTE201703_00030_165722_11750 自然语言 理解 和 生成 是 一个 多方面 问题 我们 对 他 可能 也 只是 部分 理解
    mike@local:~/src/kaldi/egs/cvte/s5/exp$

可以看到，识别效果还是相当好的。

缺点：
加载比较慢，导致整个识别过程比较慢

2、使用自定义脚本进行识别

具体如下：

::

    mike@local:demo1$ pwd
    /home/mike/src/kaldi/egs/cvte/s5/demo1
    mike@local:demo1$ cat run.sh
    #! /bin/bash

    cd /home/mike/src/kaldi/egs/cvte/s5
    . ./cmd.sh
    . ./path.sh

    demo1/nnet3-latgen-faster --frame-subsampling-factor=3 --frames-per-chunk=50 --extra-left-context=0 --extra-right-context=0 --extra-left-context-initial=-1 --extra-right-context-final=-1 --minimize=false --max-active=7000 --min-active=200 --beam=15.0 --lattice-beam=8.0 --acoustic-scale=1.0 --allow-partial=true --word-symbol-table=exp/chain/tdnn/graph/words.txt exp/chain/tdnn/final.mdl exp/chain/tdnn/graph/HCLG.fst "ark,s,cs:apply-cmvn --norm-means=true --norm-vars=false --utt2spk=ark:data/fbank/test/utt2spk scp:data/fbank/test/cmvn.scp scp:data/fbank/test/feats.scp ark:- |" "ark:|lattice-scale --acoustic-scale=10.0 ark:- ark:- | gzip -c >exp/chain/tdnn/decode_test/lat.1.gz"


    mike@local:demo1$
    mike@local:demo1$ cat update.sh
    #!/bin/bash

    cd /home/mike/src/kaldi/egs/cvte/s5
    . ./cmd.sh
    . ./path.sh

    # step 1: generate fbank features
    obj_dir=data/fbank

    for x in test; do
      # rm fbank/$x
      mkdir -p fbank/$x

      # compute fbank without pitch
      steps/make_fbank.sh --nj 1 --cmd "run.pl" $obj_dir/$x exp/make_fbank/$x fbank/$x || exit 1;
      # compute cmvn
      steps/compute_cmvn_stats.sh $obj_dir/$x exp/fbank_cmvn/$x fbank/$x || exit 1;
    done

    mike@local:demo1$


需要修改 nnet3-latgen-faster.cc 文件，代码路径：/home/mike/src/kaldi/src/nnet3bin/nnet3-latgen-faster.cc


主要是这个调用比较慢：
::

    fst::ReadFstKaldiGeneric(fst_in_str)

加载后连续识别即可，修改后的测试代码：
::

      KALDI_LOG << "before load model :"<<time(NULL);
      // Input FST is just one FST, not a table of FSTs.
      Fst<StdArc> *decode_fst = fst::ReadFstKaldiGeneric(fst_in_str);
      KALDI_LOG << "load model ok :"<<time(NULL);
      timer.Reset();

      int i = 0;
      while(1){
        clock_t start, finish;
        start = clock();
        i = i+1;
        system("bash /home/mike/src/kaldi/egs/cvte/s5/demo1/update.sh  >/dev/null 2>&1 &");
        KALDI_LOG << "decode i = "<<i<<",timestamp :"<<time(NULL);
        LatticeFasterDecoder decoder(*decode_fst, config);
        SequentialBaseFloatMatrixReader feature_reader(feature_rspecifier);

        for (; !feature_reader.Done(); feature_reader.Next()) {
          std::string utt = feature_reader.Key();
          const Matrix<BaseFloat> &features (feature_reader.Value());
          if (features.NumRows() == 0) {
            KALDI_WARN << "Zero-length utterance: " << utt;
            num_fail++;
            continue;
          }
          const Matrix<BaseFloat> *online_ivectors = NULL;
          const Vector<BaseFloat> *ivector = NULL;
          if (!ivector_rspecifier.empty()) {
            if (!ivector_reader.HasKey(utt)) {
              KALDI_WARN << "No iVector available for utterance " << utt;
              num_fail++;
              continue;
            } else {
              ivector = &ivector_reader.Value(utt);
            }
          }
          if (!online_ivector_rspecifier.empty()) {
            if (!online_ivector_reader.HasKey(utt)) {
              KALDI_WARN << "No online iVector available for utterance " << utt;
              num_fail++;
              continue;
            } else {
              online_ivectors = &online_ivector_reader.Value(utt);
            }
          }

          DecodableAmNnetSimple nnet_decodable(
              decodable_opts, trans_model, am_nnet,
              features, ivector, online_ivectors,
              online_ivector_period, &compiler);

          double like;
          if (DecodeUtteranceLatticeFaster(
                  decoder, nnet_decodable, trans_model, word_syms, utt,
                  decodable_opts.acoustic_scale, determinize, allow_partial,
                  &alignment_writer, &words_writer, &compact_lattice_writer,
                  &lattice_writer,
                  &like)) {
            tot_like += like;
            frame_count += nnet_decodable.NumFramesReady();
            num_success++;
          } else num_fail++;
        }
        finish = clock();
        KALDI_LOG << "decode i = "<<i<<",timestamp :"<<time(NULL)<<",diff :"<<(double)(finish - start) / CLOCKS_PER_SEC <<"s";
        printf("preess Enter to continue");
        getchar();
      }


测试效果：
::

    LOG (nnet3-latgen-faster[5.5.421~1453-85d1a]:main():nnet3-latgen-faster.cc:202) decode i = 1,timestamp :1567735067,diff :0.817448s
    preess Enter to continue
    LOG (nnet3-latgen-faster[5.5.421~1453-85d1a]:main():nnet3-latgen-faster.cc:151) decode i = 2,timestamp :1567735237
    apply-cmvn --norm-means=true --norm-vars=false --utt2spk=ark:data/fbank/test/utt2spk scp:data/fbank/test/cmvn.scp scp:data/fbank/test/feats.scp ark:-
    LOG (apply-cmvn[5.5.421~1453-85d1a]:main():apply-cmvn.cc:162) Applied cepstral mean normalization to 1 utterances, errors on 0
    CVTE201703_00030_165722_11750 自然语言 理解 和 生成 是 一个 多方面 问题 我们 对 他 可能 也 只是 部分 理解
    LOG (nnet3-latgen-faster[5.5.421~1453-85d1a]:DecodeUtteranceLatticeFaster():decoder-wrappers.cc:289) Log-like per frame for utterance CVTE201703_00030_165722_11750 is 2.32415 over 242 frames.
    LOG (nnet3-latgen-faster[5.5.421~1453-85d1a]:main():nnet3-latgen-faster.cc:202) decode i = 2,timestamp :1567735238,diff :0.845735s
    preess Enter to continue


可以看到，识别效果还是相当好的。
当然，这个只是测试，替换文件后，直接按回车进行识别，能达到预期效果。如果需要在实际项目中使用，上述代码做的远远不够。

本文中涉及训练数据及测试示例地址：https://pan.baidu.com/s/1jyeWkZvU8ZjLt4Y9y9B89g

可关注微信公众号后回复 19102601 获取提取码



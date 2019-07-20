var ETJS = (function(etjs) {

  etjs.bleu_score = function(sentence, reference, N) {
  /**Calculates the Bleu score between the sentence and a the reference. 
   *
   * Args:
   *     sentence: A string of words.
   *     reference: A string of words.
   *
   * Returns:
   *     The bleu-N score between the sentence and reference [0, 1].
   **/
    var matched = 0;
    var total = 0;
    for (var n = 1; n <= N; n++) {
      for (var s_index = 0; s_index + n <= sentence.length; s_index = s_index + n) {
        for (var r_index = 0; r_index + n <= reference.length; r_index = r_index + n) {
          all_matched = true;
          for (var offset = 0; offset < n; offset++) {
            //console.log(s_index+"::"+r_index+"::"+s_elem +"::"+r_elem+"::"+sentence[s_elem] + "::" + reference[r_elem])
            if (sentence[s_index + offset] != reference[r_index + offset]) {
              all_matched = false;
              break;
            }
          }
          if (all_matched) {
            matched += 1;
            break;
          }
        }
        total += 1
      }
    }
    return (matched)/total;
  }


  etjs.max_bleu_score = function(sentence, references, N) {
  /** Calculates the maximum Bleu score between a sentence and a set of references.
   *
   * Args:
   *     sentence: A string of words.
   *     references: A list of strings of words.
   *
   * Returns:
   *     The bleu-N score between the sentence and references [0, 1].
   **/
      if (sentence == undefined || sentence.length == 0) {
          return 0;
      }
      var score = 0;
      var s = sentence.toLowerCase().split(" ");
      for (var index in references) {
          var ref = references[index];
          if (ref == undefined || ref.length == 0) {
              continue;
          }
          ref = ref.toLowerCase().split(" ");
          score = Math.max(score, vg.bleu_score(s, ref, N));
      }
      return score
  };


  etjs.is_unique_sentence = function(sentence, references, threshold, N) {
  /** Decides if the sentence is new, which is decided based on if:
   *  Bleu-N(sentence, references) > threshold.
   *
   *  Args:
   *     sentence: A string of words.
   *     references: A list of strings of words.
   *     threshold: A float between [0, 1].
   *     N: Positive Integer.
   *
   * Returns:
   *     A boolean indicates if the sentence is unlike the references.
   **/
      var score = vg.max_bleu_score(sentence, references, N);
      return score < threshold;
  };


  return etjs;
}(ETJS || {}));

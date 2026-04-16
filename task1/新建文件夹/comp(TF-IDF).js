// ------------------------------
// 业务逻辑：技能 → 岗位匹配（TF-IDF 完整版）
// 真正实现：TF 结果 × IDF 结果
// ------------------------------

// 1. 计算 TF：词频（技能在当前岗位里的频率）
function computeTF(words) {
  const total = words.length;
  const freq = {};
  words.forEach(word => {
    freq[word] = (freq[word] || 0) + 1 / total;
  });
  return freq;
}

// 2. 计算 IDF：逆文档频率（技能在所有岗位里的稀有度）
function computeIDF(jobList) {
  const totalJobs = jobList.length;
  const docCount = {};

  // 统计每个技能被多少岗位需要
  jobList.forEach(job => {
    new Set(job.req).forEach(skill => {
      docCount[skill] = (docCount[skill] || 0) + 1;
    });
  });

  // 计算 IDF
  const idf = {};
  for (const skill in docCount) {
    idf[skill] = Math.log(totalJobs / (docCount[skill] + 1));
  }
  return idf;
}

// ------------------------------
// 3. 最终匹配算法（真正 TF × IDF）
// ------------------------------
function matchJob(userSkills, jobList) {
  const idfAll = computeIDF(jobList); // 全局IDF
  let bestJob = null;
  let bestScore = 0;

  // 遍历每个岗位
  jobList.forEach(job => {
    const jobSkills = job.req;
    const tf = computeTF(jobSkills); // 岗位技能的 TF
    let totalScore = 0;

    // 遍历岗位要求的每个技能
    jobSkills.forEach(skill => {
      // 如果用户会这个技能 → 加分 = TF × IDF
      if (userSkills.includes(skill)) {
        const tfValue = tf[skill];
        const idfValue = idfAll[skill] || 0;
        totalScore += tfValue * idfValue; // ✅ 真正 TF × IDF
      }
    });

    // 找出分数最高的岗位
    if (totalScore > bestScore) {
      bestScore = totalScore;
      bestJob = job;
    }
  });

  return {
    job: bestJob,
    score: bestScore.toFixed(3)
  };
}
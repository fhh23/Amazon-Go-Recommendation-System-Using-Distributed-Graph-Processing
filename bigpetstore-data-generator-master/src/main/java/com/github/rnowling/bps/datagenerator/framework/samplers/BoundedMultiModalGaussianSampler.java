/**
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package com.github.rnowling.bps.datagenerator.framework.samplers;

import java.util.List;
import java.util.Random;

import com.github.rnowling.bps.datagenerator.datamodels.Pair;
import com.github.rnowling.bps.datagenerator.framework.SeedFactory;
import com.google.common.collect.ImmutableList;

public class BoundedMultiModalGaussianSampler implements Sampler<Double>
{
	ImmutableList<Pair<Double, Double>> distributions;
	
	double min;
	double max;
	Random rng;
	
	public BoundedMultiModalGaussianSampler(List<Pair<Double, Double>> distributions, double min, double max, SeedFactory seedFactory)
	{
		rng = new Random(seedFactory.getNextSeed());
		this.distributions = ImmutableList.copyOf(distributions);
		
		this.min = min;
		this.max = max;
	}
	
	public Double sample()
	{
		int idx = rng.nextInt(distributions.size());
		
		double mean = distributions.get(idx).getFirst();
		double std = distributions.get(idx).getSecond();
		
		double value = mean + rng.nextGaussian() * std;
		
		value = Math.min(value, this.max);
		value = Math.max(value, this.min);
		
		return value;
	}

}

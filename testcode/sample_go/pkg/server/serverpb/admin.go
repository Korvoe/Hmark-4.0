// Copyright 2018 The Cockroach Authors.
//
// Use of this software is governed by the Business Source License
// included in the file licenses/BSL.txt.
//
// As of the Change Date specified in that file, in accordance with
// the Business Source License, use of this software will be governed
// by the Apache License, Version 2.0, included in the file
// licenses/APL.txt.

package serverpb

// Add adds values from ots to ts.
func (ts *TableStatsResponse) Add(ots *TableStatsResponse) {
	ts.RangeCount += ots.RangeCount
	ts.ReplicaCount += ots.ReplicaCount
	ts.ApproximateDiskBytes += ots.ApproximateDiskBytes
	ts.Stats.Add(ots.Stats)

	// The stats in TableStatsResponse were generated by getting separate stats
	// for each node, then aggregating them into TableStatsResponse.
	// So resulting NodeCount should be the same, unless ots contains nodeData
	// in MissingNodes that isn't already tracked in ts.MissingNodes.
	// Note: when comparing missingNode objects, there's a chance that the nodeId
	// could be the same, but that the error messages differ. Keeping the first
	// and dropping subsequent ones seems reasonable to do, and is what is done
	// here.
	missingNodeIds := make(map[string]struct{})
	for _, nodeData := range ts.MissingNodes {
		missingNodeIds[nodeData.NodeID] = struct{}{}
	}
	for _, nodeData := range ots.MissingNodes {
		if _, found := missingNodeIds[nodeData.NodeID]; !found {
			ts.MissingNodes = append(ts.MissingNodes, nodeData)
			ts.NodeCount--
		}
	}
}

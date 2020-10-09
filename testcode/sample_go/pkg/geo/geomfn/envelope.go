// Copyright 2020 The Cockroach Authors.
//
// Use of this software is governed by the Business Source License
// included in the file licenses/BSL.txt.
//
// As of the Change Date specified in that file, in accordance with
// the Business Source License, use of this software will be governed
// by the Apache License, Version 2.0, included in the file
// licenses/APL.txt.

package geomfn

import (
	"github.com/cockroachdb/cockroach/pkg/geo"
	"github.com/twpayne/go-geom"
)

// Envelope forms an envelope (compliant with the OGC spec) of the given Geometry.
// It uses the bounding box to return a Polygon, but can return a Point or
// Line if the bounding box is degenerate and not a box.
func Envelope(g *geo.Geometry) (*geo.Geometry, error) {
	if g.Empty() {
		return g, nil
	}
	bbox := g.CartesianBoundingBox()
	if bbox.LoX == bbox.HiX && bbox.LoY == bbox.HiY {
		return geo.NewGeometryFromGeomT(
			geom.NewPointFlat(geom.XY, []float64{bbox.LoX, bbox.LoY}).SetSRID(int(g.SRID())),
		)
	}
	if bbox.LoX == bbox.HiX || bbox.LoY == bbox.HiY {
		return geo.NewGeometryFromGeomT(
			geom.NewLineStringFlat(
				geom.XY,
				[]float64{
					bbox.LoX, bbox.LoY,
					bbox.HiX, bbox.HiY,
				},
			).SetSRID(int(g.SRID())),
		)
	}
	return geo.NewGeometryFromGeomT(
		geom.NewPolygonFlat(
			geom.XY,
			[]float64{
				bbox.LoX, bbox.LoY,
				bbox.LoX, bbox.HiY,
				bbox.HiX, bbox.HiY,
				bbox.HiX, bbox.LoY,
				bbox.LoX, bbox.LoY,
			},
			[]int{10},
		).SetSRID(int(g.SRID())),
	)
}


 	// Bail early if there's no overlap with the secondary tenant keyspace.
 	searchSpan := roachpb.Span{Key: startKey.AsRawKey(), EndKey: endKey.AsRawKey()}
 	tenantSpan := roachpb.Span{Key: keys.TenantTableDataMin, EndKey: keys.TenantTableDataMax}
 	if !searchSpan.Overlaps(tenantSpan) {
 		return nil
 	}
 
 	// Determine tenant ID range being searched: [lowTenID, highTenID].
 	var lowTenID, highTenID roachpb.TenantID
 	if searchSpan.Key.Compare(tenantSpan.Key) < 0 {
 		// startKey before tenant keyspace.
 		lowTenID = roachpb.MinTenantID
 	} else {
 		// MakeTenantPrefix(lowTenIDExcl) is either the start key of this key
 		// range or is outside of this key range. We're only searching for split
 		// points within the specified key range, so the first tenant ID that we
 		// would consider splitting on is the following ID.
 		_, lowTenIDExcl, err := keys.DecodeTenantPrefix(searchSpan.Key)
 		if err != nil {
 			log.Errorf(ctx, "unable to decode tenant ID from start key: %s", err)
 			return nil
 		}
 		if lowTenIDExcl == roachpb.MaxTenantID {
 			// MaxTenantID already split or outside range.
 			return nil
 		}
 		lowTenID = roachpb.MakeTenantID(lowTenIDExcl.ToUint64() + 1)
 	}
 	if searchSpan.EndKey.Compare(tenantSpan.EndKey) >= 0 {
 		// endKey after tenant keyspace.
 		highTenID = roachpb.MaxTenantID
 	} else {
 		rem, highTenIDExcl, err := keys.DecodeTenantPrefix(searchSpan.EndKey)
 		if err != nil {
 			log.Errorf(ctx, "unable to decode tenant ID from end key: %s", err)
 			return nil
 		}
 		if len(rem) == 0 {
 			// MakeTenantPrefix(highTenIDExcl) is the end key of this key range.
 			// The key range is exclusive but we're looking for an inclusive
 			// range of tenant IDs, so the last tenant ID that we would consider
 			// splitting on is the previous ID.
 			//
 			// Unlike with searchSpan.Key and MaxTenantID, there is no exception
 			// for DecodeTenantPrefix(searchSpan.EndKey) == MinTenantID. This is
 			// because tenantSpan.Key is set to MakeTenantPrefix(MinTenantID),
 			// so we would have already returned early in that case.
 			highTenID = roachpb.MakeTenantID(highTenIDExcl.ToUint64() - 1)
 		} else {
 			highTenID = highTenIDExcl
 		}
 	}
 
 	// Bail if there is no chance of any tenant boundaries between these IDs.
 	if lowTenID.ToUint64() > highTenID.ToUint64() {
 		return nil
 	}
 
 	// Search for the tenants table entries in the SystemConfig within the
 	// desired tenant ID range.
 	lowBound := keys.SystemSQLCodec.TenantMetadataKey(lowTenID)
 	lowIndex := s.getIndexBound(lowBound)
 	if lowIndex == len(s.Values) {
 		// No keys within range found.
 		return nil
 	}
 
 	// Choose the first key in this range. Extract its tenant ID and check
 	// whether its within the desired tenant ID range.
 	splitKey := s.Values[lowIndex].Key
 	splitTenID, err := keys.SystemSQLCodec.DecodeTenantMetadataID(splitKey)
 	if err != nil {
 		log.Errorf(ctx, "unable to decode tenant ID from system config: %s", err)
 		return nil
 	}
 	if splitTenID.ToUint64() > highTenID.ToUint64() {
 		// No keys within range found.
 		return nil
 	}
 	return roachpb.RKey(keys.MakeTenantPrefix(splitTenID))
 
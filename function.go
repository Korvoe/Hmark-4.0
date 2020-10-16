
 	undo := map[string]*string{}
 	for key, value := range kv {
 		val, ok := os.LookupEnv(key)
 		if ok {
 			undo[key] = &val
 		} else {
 			undo[key] = nil
 		}
 
 		if err := os.Setenv(key, value); err != nil {
 			panic(err)
 		}
 	}
 	return func() {
 		for key, value := range undo {
 			if value != nil {
 				if err := os.Setenv(key, *value); err != nil {
 					panic(err)
 				}
 			} else {
 				if err := os.Unsetenv(key); err != nil {
 					panic(err)
 				}
 			}
 		}
 	}
 
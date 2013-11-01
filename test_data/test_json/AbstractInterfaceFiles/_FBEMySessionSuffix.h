//
//  _FBEMySessionSuffix.h
//
//  Created by MetaJSONParser.
//  Copyright (c) 2013 SinnerSchrader Mobile. All rights reserved.

#import <Foundation/Foundation.h>

@class FBEMySessionSuffix;

@interface _FBEMySessionSuffix : NSObject <NSCoding>


// session string after login
@property (nonatomic, strong) NSString *sessionID;
// Experation date of session
@property (nonatomic, strong) NSDate *expirationDate;

+ (FBEMySessionSuffix *)mySessionWithDictionary:(NSDictionary *)dic withError:(NSError **)error;
- (id)initWithDictionary:(NSDictionary *)dic withError:(NSError **)error;
- (NSDictionary *)propertyDictionary;

@end


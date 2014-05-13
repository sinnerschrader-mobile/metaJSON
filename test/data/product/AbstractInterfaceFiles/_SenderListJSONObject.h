//
//  _SenderListJSONObject.h
//
//  Created by MetaJSONParser.
//  Copyright (c) 2014 SinnerSchrader Mobile. All rights reserved.

#import <Foundation/Foundation.h>

@class SenderJSONObject;

@class SenderListJSONObject;

@interface _SenderListJSONObject : NSObject <NSCoding>


// the title of sender list
@property (nonatomic, strong) NSString *listTitle;
// the array of Sender
@property (nonatomic, strong) NSArray *senders;

+ (SenderListJSONObject *)senderListWithDictionary:(NSDictionary *)dic withError:(NSError **)error;
- (id)initWithDictionary:(NSDictionary *)dic withError:(NSError **)error;
- (NSDictionary *)propertyDictionary;

@end


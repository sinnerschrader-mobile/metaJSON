//
//  _ProductDetailJSONObject.m
//
//  Created by MetaJSONParser.
//  Copyright (c) 2014 SinnerSchrader Mobile. All rights reserved.

#import "APIParser.h"
#import "NSString+RegExValidation.h"
#import "ProductDetailJSONObject.h"
#import "SenderGroupJSONObject.h"


@implementation _ProductDetailJSONObject

#pragma mark - factory

+ (ProductDetailJSONObject *)ProductDetailWithDictionary:(NSDictionary *)dic withError:(NSError **)error
{
    return [[ProductDetailJSONObject alloc] initWithDictionary:dic withError:error];
}


#pragma mark - initialize
- (id)initWithDictionary:(NSDictionary *)dic  withError:(NSError **)error
{
    self = [super init];
    if (self) {
        self.type = [APIParser numberFromResponseDictionary:dic forKey:@"type" acceptNil:NO error:error];
        if (*error) {
            return self;
        }
        self.advantage = [APIParser numberFromResponseDictionary:dic forKey:@"advantage" acceptNil:NO error:error];
        if (*error) {
            return self;
        }
        self.teaserURL = [APIParser stringFromResponseDictionary:dic forKey:@"teaserURL" acceptNumber:NO acceptNil:NO error:error];
        if (*error) {
            return self;
        }
        self.telephoneFlatrate = [APIParser stringFromResponseDictionary:dic forKey:@"telephoneFlatrate" acceptNumber:NO acceptNil:YES error:error];
        if (*error) {
            return self;
        }
        self.includeHardware = [APIParser boolFromResponseDictionary:dic forKey:@"includeHardware" acceptNil:NO error:error];
        if (*error) {
            return self;
        }
        NSDictionary *tmpSenderInfo = [APIParser dictionaryFromResponseDictionary:dic forKey:@"senderInfo" acceptNil:YES error:error];
        if (*error) {
            return self;
        }
        if (tmpSenderInfo) {
            self.senderInfo= [[SenderGroupJSONObject alloc] initWithDictionary:tmpSenderInfo withError:error];
            if (*error) {
                return self;
            }
        }
        self.anyProperty = [APIParser objectFromResponseDictionary:dic forKey:@"anyProperty" acceptNil:NO error:error];
        if (*error) {
            return nil;
        }
        self.title = [APIParser objectFromResponseDictionary:dic forKey:@"title" acceptNil:NO error:error];
        if (*error) {
            return nil;
        }
        self.download = [APIParser objectFromResponseDictionary:dic forKey:@"download" acceptNil:NO error:error];
        if (*error) {
            return nil;
        }
        self.upload = [APIParser objectFromResponseDictionary:dic forKey:@"upload" acceptNil:NO error:error];
        if (*error) {
            return nil;
        }
    }
    return self;
}

#pragma mark - getter

- (NSString *)titleAsTitleString:(NSError **)error
{
    if (!self.title) return nil;
    NSDictionary *newtitleDic = @{@"title" : self.title};
    NSString *tmpTitle = [APIParser stringFromResponseDictionary:newtitleDic forKey:@"title" acceptNumber:NO acceptNil:NO error:error];
    if (*error) {
        return nil;
    }
    if (tmpTitle == nil) {
        return nil;
    }
    if (tmpTitle.length > 20) {
        NSDictionary *userInfo = @{@"propertyName" : @"titleString",
                                   @"key" : @"titleString",
                                   @"reason" : @"max length validation error",
                                   @"objectClass" : NSStringFromClass([self class])
                                   };
        *error = [NSError errorWithDomain:kErrorDomain_parser code:kErrorDomain_parser_valueIsNotValid userInfo:userInfo];
        NSLog(@"%@", *error);
        return nil;
    }
    if (tmpTitle.length < 10) {
        NSDictionary *userInfo = @{@"propertyName" : @"titleString",
                                   @"key" : @"titleString",
                                   @"reason" : @"min length validation error",
                                   @"objectClass" : NSStringFromClass([self class])
                                   };
        *error = [NSError errorWithDomain:kErrorDomain_parser code:kErrorDomain_parser_valueIsNotValid userInfo:userInfo];
        NSLog(@"%@", *error);
        return nil;
    }
    if (tmpTitle && [tmpTitle matchesRegExString:@"[a-z0-9]:10"] == NO) {
        NSDictionary *userInfo = @{@"propertyName" : @"titleString",
                                   @"key" : @"titleString",
                                   @"reason" : @"validation error",
                                   @"objectClass" : NSStringFromClass([self class])
                                   };
        *error = [NSError errorWithDomain:kErrorDomain_parser code:kErrorDomain_parser_valueIsNotValid userInfo:userInfo];
        NSLog(@"%@", *error);
        return nil;
    }
    return tmpTitle;
}

- (NSString *)titleAsString:(NSError **)error
{
    if (!self.title) return nil;
    NSDictionary *newtitleDic = @{@"title" : self.title};
    NSString *tmpTitle = [APIParser stringFromResponseDictionary:newtitleDic forKey:@"title" acceptNumber:NO acceptNil:NO error:error];
    if (*error) {
        return nil;
    }
    return tmpTitle;
}

- (NSNumber *)downloadAsNumber:(NSError **)error
{
    if (!self.download) return nil;
    NSDictionary *newdownloadDic = @{@"download" : self.download};
    NSNumber *tmpDownload = [APIParser numberFromResponseDictionary:newdownloadDic forKey:@"download" acceptNil:NO error:error];
    if (*error) {
        return nil;
    }
    return tmpDownload;
}

- (NSString *)downloadAsString:(NSError **)error
{
    if (!self.download) return nil;
    NSDictionary *newdownloadDic = @{@"download" : self.download};
    NSString *tmpDownload = [APIParser stringFromResponseDictionary:newdownloadDic forKey:@"download" acceptNumber:NO acceptNil:NO error:error];
    if (*error) {
        return nil;
    }
    return tmpDownload;
}

- (NSNumber *)uploadAsNumber:(NSError **)error
{
    if (!self.upload) return nil;
    NSDictionary *newuploadDic = @{@"upload" : self.upload};
    NSNumber *tmpUpload = [APIParser numberFromResponseDictionary:newuploadDic forKey:@"upload" acceptNil:NO error:error];
    if (*error) {
        return nil;
    }
    return tmpUpload;
}

- (NSString *)uploadAsString:(NSError **)error
{
    if (!self.upload) return nil;
    NSDictionary *newuploadDic = @{@"upload" : self.upload};
    NSString *tmpUpload = [APIParser stringFromResponseDictionary:newuploadDic forKey:@"upload" acceptNumber:NO acceptNil:NO error:error];
    if (*error) {
        return nil;
    }
    return tmpUpload;
}

#pragma mark - NSCoding

- (void)encodeWithCoder:(NSCoder*)coder
{
    [super encodeWithCoder:coder];
    [coder encodeObject:self.type forKey:@"type"];
    [coder encodeObject:self.advantage forKey:@"advantage"];
    [coder encodeObject:self.teaserURL forKey:@"teaserURL"];
    [coder encodeObject:self.telephoneFlatrate forKey:@"telephoneFlatrate"];
    [coder encodeBool:self.includeHardware forKey:@"includeHardware"];
    [coder encodeObject:self.senderInfo forKey:@"senderInfo"];
    [coder encodeObject:self.anyProperty forKey:@"anyProperty"];
    [coder encodeObject:self.title forKey:@"title"];
    [coder encodeObject:self.download forKey:@"download"];
    [coder encodeObject:self.upload forKey:@"upload"];
}

- (id)initWithCoder:(NSCoder *)coder
{
    self = [super initWithCoder:coder];
    self.type = [coder decodeObjectForKey:@"type"];
    self.advantage = [coder decodeObjectForKey:@"advantage"];
    self.teaserURL = [coder decodeObjectForKey:@"teaserURL"];
    self.telephoneFlatrate = [coder decodeObjectForKey:@"telephoneFlatrate"];
    self.includeHardware = [coder decodeBoolForKey:@"includeHardware"];
    self.senderInfo = [coder decodeObjectForKey:@"senderInfo"];
    self.anyProperty = [coder decodeObjectForKey:@"anyProperty"];
    self.title = [coder decodeObjectForKey:@"title"];
    self.download = [coder decodeObjectForKey:@"download"];
    self.upload = [coder decodeObjectForKey:@"upload"];
    return self;
}

#pragma mark - Object Info
- (NSDictionary *)propertyDictionary
{
    NSMutableDictionary *dic = [[NSMutableDictionary alloc] init];
    if (self.type) {
        [dic setObject:self.type forKey:@"type"];
    }
    if (self.advantage) {
        [dic setObject:self.advantage forKey:@"advantage"];
    }
    if (self.teaserURL) {
        [dic setObject:self.teaserURL forKey:@"teaserURL"];
    }
    if (self.telephoneFlatrate) {
        [dic setObject:self.telephoneFlatrate forKey:@"telephoneFlatrate"];
    }
    if (self.includeHardware) {
        [dic setObject:[NSNumber numberWithBool:self.includeHardware] forKey:@"includeHardware"];
    }
    if (self.senderInfo) {
        [dic setObject:[self.senderInfo propertyDictionary] forKey:@"senderInfo"];
    }
    if (self.anyProperty) {
        [dic setObject:self.anyProperty forKey:@"anyProperty"];
    }
    if (self.title) {
        [dic setObject:self.title forKey:@"title"];
    }
    if (self.download) {
        [dic setObject:self.download forKey:@"download"];
    }
    if (self.upload) {
        [dic setObject:self.upload forKey:@"upload"];
    }
    return dic;
}
- (NSString *)description
{
    return [[self propertyDictionary] description];
}

@end
